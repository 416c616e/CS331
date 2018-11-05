#include <iostream>
#include "RandomPlayer.h"

RandomPlayer::RandomPlayer(char symb) : Player(symb) {

}

RandomPlayer::~RandomPlayer() {

}

void RandomPlayer::get_move(OthelloBoard* b, int& col, int& row) {
	row = rand() % b->get_num_rows();
    col = rand() % b->get_num_cols();
}

RandomPlayer* RandomPlayer::clone() {
	RandomPlayer *result = new RandomPlayer(symbol);
	return result;
}
