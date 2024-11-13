
from pyparrot.Bebop import Bebop
import time

class DroneController:
    def __init__(self):
         # Cooldown Period between inputs
        self.takeoff_cooldown = 1.0  # Reduced to 1 second for faster response
        self.last_takeoff_time = 0
        self.is_flying = False  # Track if the drone is currently flying
        self.current_altitude = 0  # Track current altitude
        self.landing_start_time = 0 #Track the time when landing is initiated 
        self.bebop = Bebop()

    def initialize(self):
        # Initialize drone connection and state
        print("Connecting")

        if self.bebop.connect(10):
            print("Successfuly connected")
            self.bebop.smart_sleep(5)
            self.bebop.ask_for_state_update()
            return True
        else: 
            print ("Failed to connect")
            return False


    def control_drone_with_gesture(self, hand_sign_id):
        landing_range = 25
        current_time = time.time()
        if hand_sign_id == 0:  # Open Hand - Takeoff or Ascend
            if not self.is_flying:  # Takeoff only if not already flying
                if current_time - self.last_takeoff_time > self.takeoff_cooldown:
                    print(f"Open Hand - Takeoff")
                    '''
                    self.bebop.safe_takeoff(10)
                    self.last_takeoff_time = current_time
                   
                    
                    '''
                    self.current_altitude = 2000  # Reset altitude on takeoff
                    self.is_flying = True  # Set flying status
            else:
                print("Open Hand - Ascending")
                '''
                self.bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=50, duration=1)  # Ascend
                self.current_altitude += 50  # Increment altitude
                '''

        elif hand_sign_id == 1:  # Closed Hand - Descend
            if self.is_flying:
                print('Closed Hand - Descending')
                '''
                self.bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-50, duration=1)  # Descend
                self.current_altitude -= 50  # Decrement altitude
                '''

                # Check if within landing range to execute landing
                if self.current_altitude <= landing_range:
                    print('Landing command executed')
                    '''
                    self.bebop.safe_land(10)
                    landing_time = current_time #record landing start time
                    self.current_altitude = 0  # Reset altitude
                    self.is_flying = False  # Update flying status
                    '''

        elif hand_sign_id == 2:  # Pointing Gesture - Forward
            if self.is_flying:
                if current_time - self.last_takeoff_time > self.takeoff_cooldown:
                    print ("Pointing - Going Forward")
                    '''
                    self.bebop.fly_direct(roll =0, pitch=50, yaw = 0, vertical_movement=0, duration=1) #Forward
                    self.last_takeoff_time = current_time
                    '''

        elif hand_sign_id == 3: # Ok Gesture - Backwards
            if self.is_flying:
                if current_time - self.last_takeoff_time > self.takeoff_cooldown:
                    '''
                    self.bebop.fly_direct(roll = 0, pitch= -50, yaw=0, vertical_movement=0, duration=1) #Backwards
                    '''
                print ("Ok - Going Backwards")

        def disconnect():
            print('disconnecting')
            self.bebop.disconnect()
            
    