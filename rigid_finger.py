import math

objects = []
springs = []

def add_object(x, halfsize, rotation=0):
    objects.append([x, halfsize, rotation])
    return len(objects) - 1

# actuation 0.0 will be translated into default actuation
def add_spring(a, b, offset_a, offset_b, length, stiffness, actuation=0.0):
    springs.append([a, b, offset_a, offset_b, length, stiffness, actuation])

def add_finger(palm, y_offset, phalanges, link_offset=0, spring_offset=0.05, tendons="Both"):

    # Figure out coordinate systems for the origin of the finger

    last_phalange_x_ = palm[0] + palm[2]
    last_phalange_y_ = palm[1] + palm[3] - y_offset

    # Store some values 

    last_l_ = palm[2]
    last_w_ = abs(palm[3]) # The absolute value allows me to skip some annoying stuff

    # Some jank required to avoid having lots of code, probably not the best
    link_iter = 1 + link_offset # This ensures springs are attached to the correct spot

    # Link counter
    phalange_cnt_ = 0

    for p_ in phalanges:

        # Extract values for easy use
        l_ = p_[0]
        w_ = p_[1]
        s_ = p_[2]

        # Add the phalanx

        add_object([last_phalange_x_ + 0.5 * l_, last_phalange_y_], [l_, w_])

        if(not(phalange_cnt_)):
            # Connect to palm
            add_spring(0, phalange_cnt_+link_iter, [ last_l_, palm[3] - y_offset], [-l_, 0.0], -1, 10 * s_)
        else:
            # Connect to other Phalanx
            add_spring(phalange_cnt_, phalange_cnt_+link_iter, [ last_l_, 0.0], [-l_, 0.0], -1, 10 * s_)
    
        # Add "tendons" 
        if(tendons == "Top" or tendons == "Both"):
            add_spring(phalange_cnt_, phalange_cnt_+link_iter, [ last_l_ - spring_offset,  last_w_], [spring_offset - l_,  w_], 2 * spring_offset, s_)
        if(tendons == "Bot" or tendons == "Both"):
            add_spring(phalange_cnt_, phalange_cnt_+link_iter, [ last_l_ - spring_offset, -last_w_], [spring_offset - l_, -w_], 2 * spring_offset, s_)

        # Update values
        last_phalange_x_ += 0.5 * l_
        last_l_ = l_
        last_w_ = w_
        phalange_cnt_ += link_iter
        link_iter = 1
        y_offset = 0.0

    # return last link index
    return phalange_cnt_

def hand(palm, phalanges_1=None, phalanges_2=None, spring_offset=0.05):

    palm_ = add_object([palm[0], palm[1]], [palm[2], palm[3]])

    # Palm always has ID of 0

    # The ID of the two tips are initalized 

    tip_id_1 = 0
    tip_id_2 = 0

    if(phalanges_1 is not None):
        tip_id_1 = add_finger(palm, phalanges_1[0][1], phalanges_1, 0, spring_offset, tendons="Bot")
    if(phalanges_2 is not None):
        tip_id_2 = add_finger([palm[0], palm[1], palm[2], -palm[3]], -phalanges_2[0][1], phalanges_2, tip_id_1, spring_offset, tendons="Top")

    return objects, springs, tip_id_1+1, tip_id_2+tip_id_1+1    