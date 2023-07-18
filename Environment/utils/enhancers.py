import numpy as np
import traci
import random as ra

from Utils.Bandwidth import Bandwidth
from Utils.Cost import RequestCost, TowerCost
from .aggregators import *
from .. import env_variables


def requests_buffering(car, observer, performance_logger):
    car.attach(observer)
    car.set_state(
        float(round(traci.vehicle.getPosition(car.id)[0], 4)),
        float(round(traci.vehicle.getPosition(car.id)[1], 4)),
    )

    # car.add_satellite(outlets[-1])
    info = car.send_request()
    if info != None:
        service = info[1][2]
        outlet = info[0]
        # print("outlet type is 1 --> : ", outlet.__class__.__name__)
        if service.request_supported(outlet):

            if outlet not in performance_logger.handled_services:
                performance_logger.set_service_handled(outlet, car, service)
            if outlet in performance_logger.handled_services:
                performance_logger.handled_services[outlet].update({car: service})

            request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
            request_cost = RequestCost(request_bandwidth, service.realtime)
            request_cost.cost_setter(service.realtime)

            if outlet not in performance_logger.outlet_services_requested_number:
                performance_logger.set_outlet_services_requested_number(
                    outlet, [0, 0, 0]
                )

            if outlet not in performance_logger.outlet_services_ensured_number:
                performance_logger.set_outlet_services_ensured_number(outlet, [0, 0, 0])

            if (
                outlet
                not in performance_logger.outlet_services_requested_number_with_action_period
            ):
                performance_logger.set_outlet_services_requested_number_with_action_period(
                    outlet, [0, 0, 0]
                )

            if (
                outlet
                not in performance_logger.outlet_services_ensured_number_with_action_period
            ):
                performance_logger.set_outlet_services_ensured_number_with_action_period(
                    outlet, [0, 0, 0]
                )

            if (
                outlet
                not in performance_logger.outlet_services_power_allocation_with_action_period
            ):
                performance_logger.set_outlet_services_power_allocation_with_action_period(
                    outlet, [0.0, 0.0, 0.0]
                )

            if (
                outlet
                not in performance_logger.outlet_services_power_allocation_current
            ):
                performance_logger.set_outlet_services_power_allocation_current(
                    outlet, [0.0, 0.0, 0.0]
                )

            if outlet not in performance_logger.outlet_services_power_allocation:
                performance_logger.set_outlet_services_power_allocation(
                    outlet, [0.0, 0.0, 0.0]
                )

            if (
                outlet
                not in performance_logger.outlet_services_power_allocation_for_all_requested
            ):
                performance_logger.set_outlet_services_power_allocation_for_all_requested(
                    outlet, [0.0, 0.0, 0.0]
                )

            service.service_power_allocate = request_bandwidth.allocated
            if len(outlet.power_distinct[0]) == 0:
                outlet.power = [0.0, 0.0, 0.0]

            tower_cost = TowerCost(request_bandwidth, service.realtime)
            tower_cost.cost_setter(service.realtime)

            services_aggregation(
                performance_logger.outlet_services_requested_number,
                outlet,
                service.__class__.__name__,
                1,
            )
            services_aggregation(
                performance_logger.outlet_services_requested_number_with_action_period,
                outlet,
                service.__class__.__name__,
                1,
            )
            power_aggregation(
                performance_logger.outlet_services_power_allocation_with_action_period,
                outlet,
                service.__class__.__name__,
                service,
                1,
            )
            power_aggregation(
                performance_logger.outlet_services_power_allocation_for_all_requested,
                outlet,
                service.__class__.__name__,
                service,
                1,
            )
            ensured_service_aggrigation(
                performance_logger.outlet_services_ensured_number_with_action_period,
                outlet,
                service.__class__.__name__,
                1,
            )


def centralize_state_action(gridcells_dqn, step, performance_logger):
    number_of_services = 3
    state = 0
    performance_logger.number_of_periods_until_now = 1
    for gridcell in gridcells_dqn:
        states = []
        actions = []
        actions_objects = []
        list_flags = []

        # if step > 2:
        #     if step > env_variables.advisor_period[0] and step <= env_variables.advisor_period[1]:
        #         flags = gridcell.agents.heuristic_action(gridcell,
        #                                                  performance_logger.outlet_services_power_allocation_for_all_requested,
        #                                                  performance_logger.outlet_services_requested_number,
        #                                                  performance_logger.number_of_periods_until_now)
        #         list_flags.extend(flags)
        for j, outlet in enumerate(gridcell.agents.grid_outlets):
            supported = []

            for i in range(number_of_services):
                gridcell.environment.state.index_outlet = j
                gridcell.environment.state.index_service = i
                if step <= 2:
                    list_flags.append(0)
                    gridcell.environment.state.max_capacity_each_outlet[
                        j
                    ] = outlet._max_capacity
                    gridcell.environment.state.capacity_each_tower[
                        j
                    ] = outlet.current_capacity
                    gridcell.environment.state.services_requested_for_outlet = (
                        outlet.dqn.environment.state.services_requested
                    )
                    gridcell.environment.state.services_ensured_for_outlet = (
                        outlet.dqn.environment.state.services_ensured
                    )
                    if len(outlet.power_distinct[0]) == 0:
                        outlet.power = [0.0, 0.0, 0.0]
                    gridcell.environment.state.allocated_power = outlet.power_distinct

                    state = gridcell.environment.state.calculate_state()
                    states.append(state)
                    action = ra.randint(0, 1)
                    actions.append(action)
                    gridcell.environment.state.supported_service = action
                    supported.append(action)

            count_zero = 0
            if step <= 2:
                for ind in range(3):
                    if supported[ind] == 0:
                        count_zero += 1
                if count_zero == 3:
                    supported[0] = 1
                outlet.supported_services = supported

            if step > 2:
                if (
                    step > env_variables.exploitation_exploration_period[0]
                    and step <= env_variables.exploitation_exploration_period[1]
                ):
                    outlet.supported_services = []
                    for serv_index in range(number_of_services):
                        action_centralize, action, flag = gridcell.agents.chain(
                            gridcell.model,
                            gridcell.environment.state.state_value_centralize[j],
                            gridcell.agents.epsilon,
                        )

                        if isinstance(action, np.ndarray):
                            action = action.item()
                        outlet.supported_services.append(action)
                        list_flags.append(flag)

                if (
                    env_variables.advisor_period[0]
                    < step
                    <= env_variables.advisor_period[1]
                ):
                    # if step > env_variables.advisor_period[0]  and  step <= env_variables.advisor_period[1]:
                    outlet.supported_services = []
                    mask = []
                    for serv_index in range(number_of_services):
                        (
                            action_centralize,
                            action,
                            flag,
                        ) = gridcell.agents.exploitation(

                            gridcell.model,
                            gridcell.environment.state.state_value_centralize[j],
                        )
                        # actions_objects.append(action_centralize)
                        if isinstance(action, np.ndarray):
                            action = action.item()
                        outlet.supported_services.append(action)
                        list_flags.append(flag)

                actions.extend(outlet.supported_services)
            # print("outlet.supported_services : ", outlet.supported_services)
            outlet.dqn.environment.state.supported_services = outlet.supported_services

        # gridcell.agents.action.command.action_objects = actions_objects
        gridcell.agents.action.command.action_value_centralize = actions
        gridcell.agents.action.command.action_flags = list_flags

        if step <= 2:
            gridcell.environment.state.state_value_centralize = states


def centralize_nextstate_reward(gridcells_dqn):
    for gridcell in gridcells_dqn:
        # print("state value centralize : ", gridcell.environment.state.state_value_centralize)
        next_states = []
        rewards = []
        utility_value_centralize = 0
        index_of_service = 0
        outlets = gridcell.agents.grid_outlets
        # for ind in outlets:
            # print(
            #     "type : ",
            #     ind.__class__.__name__,
            #     "  current capacity : ",
            #     ind.current_capacity,
            # )
        index_of_outlet = -1
        for i in range(9):
            index_of_service = i % 3
            if i % 3 == 0:
                index_of_outlet += 1

            gridcell.environment.state.index_service = index_of_service
            gridcell.environment.state.index_outlet = index_of_outlet
            gridcell.environment.state.max_capacity_each_outlet[
                index_of_service
            ] = outlets[index_of_outlet]._max_capacity
            gridcell.environment.state.capacity_each_tower[index_of_service] = outlets[
                index_of_outlet
            ].current_capacity
            gridcell.environment.state.services_requested_for_outlet = outlets[
                index_of_outlet
            ].dqn.environment.state.services_requested
            gridcell.environment.state.services_ensured_for_outlet = outlets[
                index_of_outlet
            ].dqn.environment.state.services_ensured
            gridcell.environment.state.allocated_power = outlets[
                index_of_outlet
            ].power_distinct
            next = gridcell.environment.state.calculate_state()
            next_states.append(next)
            # print("next state value centralize : ", next)

        rewards = gridcell.environment.reward.calculate_reward()

        gridcell.environment.state.next_state_centralize = next_states
        gridcell.environment.reward.reward_value = rewards
        # for index in range(9):
        #     gridcell.agents.remember(gridcell.agents.action.command.action_flags[index],
        #                              gridcell.environment.state.state_value_centralize[index],
        #                              gridcell.agents.action.command.action_value_centralize[index],
        #                              gridcell.environment.reward.reward_value[index],
        #                              gridcell.environment.state.next_state_centralize[index])

        gridcell.environment.state.state_value_centralize = (
            gridcell.environment.state.next_state_centralize
        )
        gridcell.environment.state.services_requested_prev = (
            gridcell.environment.state.services_requested
        )
        gridcell.environment.reward.services_requested_prev = (
            gridcell.environment.reward.services_requested
        )
        gridcell.environment.state.services_ensured_prev = (
            gridcell.environment.state.services_ensured
        )
        gridcell.environment.reward.services_ensured_prev = (
            gridcell.environment.reward.services_ensured
        )
        gridcell.environment.state.utility_value_centralize_prev = (
            utility_value_centralize
        )
        gridcell.environment.reward.utility_value_centralize_prev = (
            utility_value_centralize
        )


def decentralize_period(performance_logger, gridcells_dqn, step):
    for gridcell in gridcells_dqn:
        req1 = np.zeros(3)
        ens1 = np.zeros(3)
        power = np.zeros(3)
        for i, outlet in enumerate(gridcell.agents.grid_outlets):
            print("outlet.dqn.environment.state.supported_services[service_index] : ",outlet.dqn.environment.state.supported_services)
            if outlet in performance_logger.handled_services:
                outlet._max_capacity = outlet.set_max_capacity(outlet.__class__.__name__)
                gridcell.environment.state._max_capacity_each_outlet[i] = outlet._max_capacity
                gridcell.environment.state._capacity_each_tower[i] = outlet.current_capacity

                outlet.dqn.environment.state.state_value_decentralize[0] = outlet.current_capacity
                outlet.dqn.environment.state.tower_capacity = outlet.current_capacity
                outlet.dqn.environment.state.max_tower_capacity = outlet._max_capacity

                outlet.dqn.environment.state.supported_services = outlet.supported_services
                outlet.dqn.environment.state.action_value = outlet.dqn.agents.action_value

                if step <= 10:
                    outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.calculate_state()
                # print("outlet.dqn.environment.state.supported_services : ",outlet.dqn.environment.state.supported_services)
                print("decentralize state : ",outlet.dqn.environment.state.state_value_decentralize)


                action_decentralize,outlet.dqn.agents.action.command.action_value_decentralize,flag = \
                    outlet.dqn.agents.chain_dec(
                    outlet.dqn.model,
                    outlet.dqn.environment.state.state_value_decentralize,
                    outlet.dqn.agents.action_masking(outlet.dqn.environment.state.supported_services),

                    outlet.dqn.agents.epsilon,
                )

                mapped_action = 0
                for key, val in outlet.dqn.agents.action_permutations_dectionary.items():
                    if val == outlet.dqn.agents.action.command.action_value_decentralize:
                        print("the key : ", key)
                        mapped_action =  key


                print("action decentralize from chain  : ", outlet.dqn.agents.action.command.action_value_decentralize)

                outlet.dqn.agents.action_value = (
                    outlet.dqn.agents.action.command.action_value_decentralize
                )

                outlet.dqn.environment.state.action_value = (
                    outlet.dqn.agents.action_value
                )
                x = 0
                for service_index,services_actions in enumerate(mapped_action) :

                    if services_actions == 1:
                        Z = outlet.current_capacity
                        C = performance_logger.outlet_services_power_allocation_with_action_period[
                                outlet][service_index]

                        print("c is : ",C)
                        print("what sum from  : ", performance_logger.outlet_services_power_allocation_with_action_period[
                                outlet
                            ][service_index])
                        if outlet.current_capacity - C <= 0:
                            outlet.current_capacity = 0
                        else:
                            outlet.current_capacity = outlet.current_capacity - C


                        x = Z - C

                        number_of_requests_in_this_period = performance_logger.outlet_services_requested_number_with_action_period[
                            outlet
                        ][
                            service_index
                        ]
                        sum_power_allocation = performance_logger.outlet_services_power_allocation_with_action_period[
                            outlet
                        ][
                            service_index
                        ]


                        if number_of_requests_in_this_period != 0:
                            outlet.dqn.environment.state.mean_power_allocated_requests = (
                                sum_power_allocation
                                / number_of_requests_in_this_period
                            )
                        else:
                            outlet.dqn.environment.state.mean_power_allocated_requests = (
                                0
                            )

                        outlet.dqn.environment.state.services_requested = performance_logger.outlet_services_requested_number_with_action_period[
                            outlet
                        ]

                        outlet.power = performance_logger.outlet_services_power_allocation_with_action_period[
                            outlet
                        ]

                        outlet.dqn.environment.state.allocated_power = outlet.power
                        print("outlet.dqn.environment.state.allocated_power  : ", outlet.dqn.environment.state.allocated_power)
                        outlet.dqn.environment.state.tower_capacity = (
                            outlet.current_capacity
                        )

                        outlet.dqn.environment.state.services_ensured = performance_logger.outlet_services_ensured_number_with_action_period[
                            outlet
                        ]

                        # for ind in range(3):
                        performance_logger.outlet_services_ensured_number[outlet][service_index] = (
                            performance_logger.outlet_services_ensured_number[outlet][service_index]
                            + outlet.dqn.environment.state.services_ensured[service_index]
                        )

                        performance_logger.outlet_services_power_allocation[outlet][service_index] = (
                            performance_logger.outlet_services_power_allocation[outlet][service_index]
                            + outlet.dqn.environment.state.allocated_power[service_index]
                        )

                    elif services_actions == 0:
                        Z = outlet.current_capacity
                        C = performance_logger.outlet_services_power_allocation_with_action_period[outlet][service_index]


                        print("c is : ", C)
                        print("what sum from  : ",
                              performance_logger.outlet_services_power_allocation_with_action_period[outlet][service_index])

                        x = Z - C
                        number_of_requests_in_this_period = performance_logger.outlet_services_requested_number_with_action_period[outlet][service_index]
                        sum_power_allocation = performance_logger.outlet_services_power_allocation_with_action_period[
                            outlet][service_index]



                        if number_of_requests_in_this_period != 0:
                            outlet.dqn.environment.state.mean_power_allocated_requests = (
                                sum_power_allocation
                                / number_of_requests_in_this_period
                            )
                        else:
                            outlet.dqn.environment.state.mean_power_allocated_requests = (
                                0
                            )

                        outlet.power = performance_logger.outlet_services_power_allocation_with_action_period[
                            outlet
                        ]

                        outlet.dqn.environment.state.allocated_power = outlet.power
                        print("outlet.dqn.environment.state.allocated_power : , ", outlet.dqn.environment.state.allocated_power)
                        outlet.dqn.environment.state.services_requested = performance_logger.outlet_services_requested_number_with_action_period[outlet]
                        outlet.dqn.environment.state.services_ensured = [0,0,0]
                        performance_logger.set_outlet_services_ensured_number_with_action_period(
                            outlet, [0, 0, 0]
                        )

                outlet.dqn.environment.state.action_value = (
                    outlet.dqn.agents.action.command.action_value_decentralize
                )
                outlet.dqn.environment.state.next_state_decentralize = action_decentralize.execute(
                    outlet.dqn.environment.state,
                    outlet.dqn.agents.action.command.action_value_decentralize,
                )


                print(
                    "decenlraize next state value :   ",
                    outlet.dqn.environment.state.next_state_decentralize,
                )

                outlet.dqn.environment.reward.reward_value = outlet.dqn.environment.reward.calculate_reward(
                    x,
                    outlet.dqn.agents.action.command.action_value_decentralize,
                    sum(
                        performance_logger.outlet_services_power_allocation_with_action_period[
                            outlet
                        ]
                    ),
                    outlet._max_capacity,
                )


                if isinstance(
                    outlet.dqn.agents.action.command.action_value_decentralize,
                    np.ndarray,
                ):
                    outlet.dqn.agents.action.command.action_value_decentralize = (
                        outlet.dqn.agents.action.command.action_value_decentralize.item()
                    )


                outlet.dqn.agents.remember_decentralize(
                    outlet.dqn.environment.state.supported_services,
                    flag,
                    outlet.dqn.environment.state.state_value_decentralize,
                    outlet.dqn.agents.action.command.action_value_decentralize,
                    outlet.dqn.environment.reward.reward_value,
                    outlet.dqn.environment.state.next_state_decentralize,
                )

                outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.next_state_decentralize

                if len(outlet.power_distinct[0]) == 0:
                    outlet.power = [0.0, 0.0, 0.0]

                outlet.distinct = gridcell.agents.outlets_id[i]
                # gridcell.environment.state.allocated_power = outlet.power_distinct
                gridcell.environment.state.supported_services = outlet.supported_services_distinct


                for service_index in range(3):
                    req1[service_index] = (
                        req1[service_index]
                        + performance_logger.outlet_services_requested_number[
                            outlet
                        ][service_index]
                    )
                    ens1[service_index] = (
                        ens1[service_index]
                        + performance_logger.outlet_services_ensured_number[outlet][
                            service_index
                        ]
                    )
                    power[service_index] = (
                        power[service_index]
                        + performance_logger.outlet_services_power_allocation[
                            outlet
                        ][service_index]
                    )


        gridcell.environment.state.services_requested = req1
        gridcell.environment.reward.services_requested = req1
        gridcell.environment.state.services_ensured = ens1
        gridcell.environment.reward.services_ensured = ens1
        gridcell.environment.state.average_power_allocate = power

