# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/api/16_airsim.commands.ipynb.

# %% auto 0
__all__ = ['logger', 'start_sim', 'DroneCommands']

# %% ../../nbs/api/16_airsim.commands.ipynb 6
from fastcore.utils import *
import UAV.airsim_python_client as airsim
from ..airsim_client import AirSimClient
import time
from ..utils.sim_linux import RunSim, is_process_running, find_and_terminate_process
import logging


# %% ../../nbs/api/16_airsim.commands.ipynb 7
logging.basicConfig(format='%(asctime)-8s,%(msecs)-3d %(levelname)5s [name] [%(filename)10s:%(lineno)3d] %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)  # Todo add this to params
logger = logging.getLogger("__name__")   # todo add this to params

# %% ../../nbs/api/16_airsim.commands.ipynb 10
def start_sim():
    """Start the Airsim simuator if it is not already running"""
    sim_name = "AirSimNH"
    if not is_process_running(f"{sim_name}"):
        return RunSim("AirSimNH", settings="config/settings_high_res.json")
    return None   

# %% ../../nbs/api/16_airsim.commands.ipynb 12
class DroneCommands():
    """Class Multirotor Client for the Airsim simulator with higher level procedures"""

    def __init__(self,
                 takeoff_z:int = -5): # takeoff Height
        self._z = takeoff_z
        self._stop = False

    def arm(self):
            """Run the drone on a path in the Airsim simulator.
            Creates a client and connects to the simulator."""
            self._client = AirSimClient()
    
            self._client.enableApiControl(True)
        
            logger.info("Arming the drone...")
            self._client.armDisarm(True)        


    def disarm(self):
        """Disarm the drone and disconnect from the simulator"""
        logger.info("disarming...")
        self._client.armDisarm(False)
        self._client.enableApiControl(False)
        
        
    def takeoff(self):
        """Takeoff to the takeoff height"""
        state = self._client.getMultirotorState()
        if state.landed_state == airsim.LandedState.Landed:
            logger.info("taking off...")
            self._client.takeoffAsync().join()
        else:
            self._client.hoverAsync().join()
    
        time.sleep(1)
    
        state = self._client.getMultirotorState()
        if state.landed_state == airsim.LandedState.Landed:
            logger.info("take off failed...")
            sys.exit(1)
    
        # AirSim uses NED coordinates so negative axis is up.
        # _z of -5 is 5 meters above the original launch point.
        # _z = -50
        print("make sure we are hovering at {} meters...".format(-self._z))
        self._client.moveToZAsync(self._z, 5).join()

    
    def do_NH_path(self):
        """Fly on a path in the Airsim simulator"""
        logger.info("flying on path...")
        print("""This script is designed to fly on the streets of the Neighborhood environment
            and assumes the unreal position of the drone is [160, -1500, 120].""")
        result = self._client.moveOnPathAsync([airsim.Vector3r(125,0,self._z),
                                        airsim.Vector3r(125,-130,self._z),
                                        airsim.Vector3r(0,-130,self._z),
                                        airsim.Vector3r(0,0,self._z)],
                                12, 120,
                                airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), 20, 1).join()
    
    def rth(self):
        logger.info("returning home...")
        # drone will over-shoot so we bring it back to the start point before landing.
        # _client.moveToPositionAsync(0,0,_z,1).join()
        self._client.goHomeAsync().join()
    
    def land(self):
        logger.info("landing...")
        self._client.landAsync().join()
    

    def do_tasklist(self):
        """Run a list of tasks in order"""
        tasks = [self.arm, self.takeoff, self.do_NH_path, self.rth, self.land, self.disarm]
        for task in tasks:
            if self._stop:
                break
            task()
                
    def stop(self):
        """ stop the client by cancelling the last task and exiting the do_tasklist loop """
        self._stop = True
        try:
            self._client.cancelLastTask()
        except Exception as e:
            print (e)

