# Different angles of different accuracies
    # accuracy falls off exponentially with distance
#   Gradient of strength using ^
#   Variable direction of focus using ^
# move the missile closer to the target if it spots it
#   animation of the missile going after stuff using ^

################################### TODO ####################################
# DOCUMENTATION
#    function input types
#    function definitions
# we got the single angle and offset and resistance and thing working
# now, work on:
#    Gradient strength
#    enemy movement prediction
#    stopping when the missile hits
#       have it check if the lines cross, not just have the same point
#       get the equations of the lines and see if you can make them equal
#       m_enemy = enemy.next_position[0]-enemy.position[0]/enemy.next_position[1]-enemy.position[1]
#       m_misle = misle.next_position[0]-misle.position[0]/misle.next_position[1]-misle.position[1]

class missile:
    def __init__(self) -> None:
        self.position = (0, 0) # grid coordinates
        self.velocity = 1 # units/frame
        self.facing = (0, 1) # what point yer facing on the unit circle
        self.get_facing_vector()

    def get_facing_vector(self):
        self.facing_vector = (self.velocity*self.facing[0]+self.position[0], self.velocity*self.facing[1]+self.position[1])
        return self.facing_vector

    def set_facing(self, degrees):
        # degrees from due east
        self.facing = missile.get_facing(degrees)
    
    def get_facing(degrees):
        # degrees from due east

        from numpy import sin, cos, radians
        angle = radians(degrees)
        output = (cos(angle), sin(angle))
        return output

    def getangle(v1, v2=(1, 0)):
        # a*b = |a||b|cos(angle)

        from numpy import arccos, degrees, dot

        adotb = dot(v1, v2)
        norma = (v1[0]**2+v1[1]**2)**(1/2)
        normb = (v2[0]**2+v2[1]**2)**(1/2)
        angle = round(degrees(arccos(adotb/(norma*normb))), 2)
        return angle
    
    def is_inrange(self, target, offset, angle):
        # the offset from where the missile is facing in degrees from straight
        # the angle that the sensing is active within
        
        target_vector = (target[0]-self.position[0], target[1]-self.position[1]) # get the vector from the position of the missile to the enemy
        
        # if the angle gets bigger as you increase turning, it's to the right(-)
        # if we set self.facing + 1 degree, and the target degree gets bigger, it's to the right

        target_angle = missile.getangle(target_vector, self.facing)

        self_angle = missile.getangle(self.facing)
        next_angle = self_angle + 1
        next_vector = missile.get_facing(next_angle)
        next_target_angle = missile.getangle(target_vector, next_vector)

        if next_target_angle > target_angle:
            target_angle = target_angle*-1

        left_angle = offset - angle/2
        right_angle = offset + angle/2
        angle_range = (left_angle, right_angle)
        if left_angle <= target_angle <= right_angle:
            out_check = True
        else:
            out_check = False
        
        return out_check, angle_range, target_angle

    def one_strength(self, metadata, enemy_position):
        (offset, sence_angle, strength, resistance) = metadata
        
        # the offset from where the missile is facing in degrees from straight
        # sence_angle is the angle that the sensing is active within
        # strength is starting accuracy (0-1) = (0%-100%)
        # resistance is how much it resists dropping off
        # distance is the distance to the target

        from random import random

        (in_check, angle_range, target_angle) = self.is_inrange(enemy_position, offset, sence_angle)
        if in_check:
            distance = ((self.position[0]-enemy_position[0])**2+(self.position[1]-enemy_position[1])**2)**(1/2)
            accuracy = strength*(2**(-((1/resistance)*distance)))
            if random() < accuracy:
                hit = True
            else:
                hit = False
        else:
            hit = False

        return hit, angle_range, target_angle
    
    def move(self, angle_range):
        from random import random
        # move towards the sense

        (left_angle, right_angle) = angle_range
        move_angle = (random()*(left_angle-right_angle))+right_angle
        self.set_facing(missile.getangle(self.facing) + move_angle)
        self.position = self.get_facing_vector()

        return self.position

    def go(self, enemy_position, metadata):
        (offset, sence_angle, strength, resistance) = metadata
        positions = [self.position]
        index = 0

        while (self.position != enemy_position) and (index<1000):
            positions.append(self.go_once(enemy_position, metadata))
            index += 1

        return positions
    
    def go_once(self, enemy_position, metadata):
        (offset, sence_angle, strength, resistance) = metadata

        (hit_check, angle_range, target_angle) = self.one_strength(metadata, enemy_position)
        if hit_check:
            variation = (sence_angle/50)/strength
            #variation = 0
            angle_range = (target_angle+variation, target_angle-variation)
            self.move(angle_range)

        return self.position

    def graphaccuracy(distance, strength, resistance):
        import matplotlib.pyplot as plt
        
        x = []
        for i in range(0, (distance*10)+1):
            x.append(i/10)
        y = []
        for item in x:
            y.append(strength*(2**(-((1/resistance)*item))))
        
        plt.plot(x, y, color='r')
        plt.xlabel('Distance from missile')
        plt.ylabel('Accuracy')
        plt.grid(visible=True, color='#e0e0e0')
        plt.xlim((0, max(x)))
        plt.ylim((0, max(y)))
        plt.show()



def first_scan(metadata, misle, enemy):
    for i in range(360):
        misle.set_facing(i+90)
        (hit_check, _, _) = misle.one_strength(metadata, enemy.position)
        #print('#', end='')
        #sleep(77/9000)
        if hit_check:
            print('\n', i)
            break

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from time import sleep
    
    #missile.graphaccuracy(10, 1, 2)

    misle = missile()
    misle.velocity = 0.125

    enemy = missile()
    enemy.position = (-10, 7)
    enemy.set_facing(270)
    enemy.velocity = 0.1
    
    metadata = (0, 90, 1, 100)
    first_scan(metadata, misle, enemy)
    
    metadata = (0, 20, 1, 100)
    misle_positions = []
    enemy_positions = []
    for i in range(5000):
        if (misle.position != enemy.position):
            misle_positions.append(misle.go_once(enemy.position, metadata))
            enemy_positions.append(enemy.move((0, 0)))
            status = 'No Hit :('
        else:
            status = f'HIT @ {(misle.position)}'
            plt.plot(misle.position[0], misle.position[1], color='y', marker='*')
    
    misx = []
    misy = []
    for i in misle_positions:
        misx.append(i[0])
        misy.append(i[1])
    plt.plot(misx, misy, color='b', marker='')
    
    enex = []
    eney = []
    for i in enemy_positions:
        enex.append(i[0])
        eney.append(i[1])
    plt.plot(enex, eney, color='r', marker='')

    print(status)
    plt.show()
