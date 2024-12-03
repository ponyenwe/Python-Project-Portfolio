from math import cos,radians,sin

class Car:
    def __init__(self,x=0.0,y=0.0,heading=0.0):
        self.x = x
        self.y = y
        self.heading = heading
        
    def turn(self, degrees):
        
        self.heading += degrees
        self.heading % 360
        
    def drive(self, distance):
        self.x += distance * sin(radians (self.heading))
        self.y -= distance * cos(radians (self.heading))
        
def sanity_check():
    car = Car()
    car.turn(90)
    car.drive(10)
    car.turn(30)
    car.drive(20)
    
    print(f"Location: {car.x},{car.y} \nHeading: {car.heading}")
    
    return car

if __name__ == "__main__":
    sanity_check()