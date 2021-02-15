#!/usr/bin/env python3
import time
from datetime import datetime
from statemachine import StateMachine
from photocapture import PhotoCapture
import asyncio
import concurrent.futures
from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan, MissionResult, MissionProgress)
from odmmanager import OdmManager
from auth import (hostname, port, token)

# Checks if the drone is landed and the mission is successful
async def check_land_position(args):
    if drone.telemetry.landed_state() is MissionResult.Result.SUCCESS:
        return True

# Handler for idle state
async def idle_state(args):
    print("-- Downloading mission")
    mission_plan = await drone.action.download_mission()
    if len(mission_plan) > 0:
        newState = "start_flight"
    else:
        print("Mission Failed")
        newState = "error_state"
    return (newState, mission_plan)

# Handler for start flight state
async def start_flight_state(args):
    print("-- Starting Mission")
    await drone.mission.start_mission()
    await asyncio.sleep(5)
    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            newState = "photo_capture"
            return (newState, args)

# Checks the progress of mission and takes photos as per mission item
async def capture_manager(args):
    async for mission_progress in drone.mission.mission_progress():
        if args.camera_action == MissionItem.CameraAction.TAKE_PHOTO:
            p.capture()
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")

# Handler for photo capture state
async def photo_capture_state(args):
    async for is_in_air in drone.telemetry.in_air():
        if not is_in_air:
            if drone.mission.is_mission_finished():
                newState = "landing"
            else:
                newState = "error_state"
                print("Mission Failed")
            return (newState, args)
        else:
            await capture_manager(args)

# Handler for landing state
async def landing_state(args):
    if check_land_position(args):
        newState = "odm_manager"
    else:
        newState = "error_state"
        print("Mission Failed")
    return (newState, args)

# Wrapped the blocking image processing function with some asyncio magig
async def wrapped_process_image():
    executor = concurrent.futures.ThreadPoolExecutor()
    await loop.run_in_executor(executor, om.processImages())

# Handler for odm manager state
async def odm_manager_state(args):
    await wrapped_process_image()
    print("Mission Successful")
    newState = "mission_end"
    return (newState, args)

# Initializes the state machine
async def init_sm():
    await m.add_state("idle", idle_state)
    await m.add_state("start_flight", start_flight_state)
    await m.add_state("photo_capture", photo_capture_state)
    await m.add_state("landing", landing_state)
    await m.add_state("odm_manager", odm_manager_state)
    await m.add_state("mission_end", None, end_state=1)
    await m.add_state("error_state", None, end_state=1)
    await m.set_start("idle")

async def run():
    await drone.connect(system_address="serial:///dev/ttymxc2:921600")
    print("Waiting for drone...")
    await asyncio.sleep(2)
    try:
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered with UUID: {state.uuid}")
                break
        print("-- Arming")
        await drone.action.arm()
        await m.run()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # Create a state machine object and initialize it
    m = StateMachine()
    p = PhotoCapture()
    p.config("images/", 640, 480, 'TestFlight1')
    om = OdmManager()
    om.config("images/*", token, hostname, port)
    drone = System()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
