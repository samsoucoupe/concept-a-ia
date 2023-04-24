import json
import xml_generator as xml_generator

initial = [0,0]
final = [4,0]
possible_value=[[0,1,2,3,4,5],[0,1,2,3]]
name_nodes = ["S5","S3"]


def generate_transition_text(current,new):
    init = " ".join([str(x) for x in current])
    final = " ".join([str(x) for x in new])
    return f"{init} {final}"


def convert_to_xml_list(current,variations):
    xml_list=[]
    for i in range(len(variations)):
        temp_txt=generate_transition_text(current,variations[i])
        xml_list.append(f"{temp_txt}")

    return xml_list


def valid_values(state,possible_value,init,actual_transition_list=[]):

    if len(state)==0 or (generate_transition_text(init,state) in actual_transition_list) or (state == init and state != final):
        return False
    for i in range(len(state)):
        if state[i] not in possible_value[i]:
            return False
    return True

def generate_variation(state,possible_value,actual_transition_list=[],final=[],init=[]):
    # pour chaque noeud
    # on peut vider, remplir ou verser

    def vider(i):
        if state[i] != 0 :
            new_state=list(state)
            new_state[i]=0
            return new_state
    def remplir(i):
        if state[i] != possible_value[i][-1]:
            new_state=list(state)
            new_state[i]=possible_value[i][-1]
            return new_state
    def verser(i,j):
        # on transfert de i vers j
        new_state=list(state)
        if new_state[i]+new_state[j] <= possible_value[j][-1] and new_state[i]  !=0 :
            new_state[j]+=new_state[i]
            new_state[i]=0
        else:
            new_state[i]-=possible_value[j][-1]-new_state[j]
            new_state[j]=possible_value[j][-1]
        return new_state

    if state == final:
        new_state=[final]
        print("final state")
        print(f"{new_state}")
    else:
        new_state=[]
        for i in range(len(state)):
            temp_state=vider(i)
            if temp_state != None:
                new_state.append(temp_state)
            temp_state=remplir(i)
            if temp_state != None:
                new_state.append(temp_state)

            for j in range(len(state)):
                if i != j:
                    temp_state=verser(i,j)
                    if temp_state != None:
                        new_state.append(temp_state)
#     on va test les nouvelles valeurs
    valid_states=[]
    temp_transition_list=actual_transition_list.copy()
    for i in range(len(new_state)):
        if valid_values(state=new_state[i],possible_value=possible_value,init=state,actual_transition_list=temp_transition_list):
            valid_states.append(new_state[i])
            temp_transition_list.append(generate_transition_text(state,new_state[i]))

    return valid_states


def generate_states(states, possible_value,xml_list=[]):
    new_states=[]
    for state in states:
        new_state=generate_variation(state=state,possible_value=possible_value,actual_transition_list=xml_list,final=final,init=initial)
        if new_state != []:
            xml_list+=convert_to_xml_list(state,new_state)
            new_states+=new_state
    return new_states,xml_list

def main(initial, final, possible_value):
    states=[initial]
    stack=[initial]
    xml_list=[]
    while stack != []:
        state=stack.pop()
        new_state=generate_variation(state=state,possible_value=possible_value,actual_transition_list=xml_list,final=final,init=initial)
        if new_state != []:
            xml_list+=convert_to_xml_list(state,new_state)
            states+=new_state
            stack+=new_state
    return states,xml_list


if __name__ == '__main__':
    states,xml_list=main(initial,final,possible_value)
    name_f="zodice"
    xml_generator.generator(name=name_f,initial=initial,final=final,possible_value=possible_value,name_nodes=name_nodes,xml_list=xml_list)





