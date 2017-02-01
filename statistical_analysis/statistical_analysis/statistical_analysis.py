from scipy.stats import ttest_ind 
from numpy import std, mean

def main():
    
    data_set_control = get_data_set(53,45,2)
    data_set_new = get_data_set(12,87,1)

    
    print(str(ttest_ind(data_set_control,data_set_new))+' mean data_set_control= '+str(mean(data_set_control))+'+-'+str(std(data_set_control))+' mean data_set_new= '+str(mean(data_set_new))+'+-'+str(std(data_set_new)))


def get_data_set(wins_player2, wins_player1, draws):#note first player 2
    total_games = wins_player2 + wins_player1 + draws;
    data_list = list(range(total_games))
    counter = 0
    for x in range(0,wins_player2):
        data_list[counter] = 1
        counter+=1
    for x in range(0,wins_player1):
        data_list[counter] = -1
        counter+=1
    for x in range(0,draws):
        data_list[counter] = 0
        counter+=1
    return data_list

if __name__ == "__main__":

    main()
