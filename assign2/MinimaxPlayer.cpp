/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include <limits.h>
#include "MinimaxPlayer.h"

using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    char currentPlayer = symbol;

	if ( currentPlayer == b->get_p1_symbol() ) {
		currentPlayer = b->get_p2_symbol();
	} else {
		currentPlayer = b->get_p1_symbol();
	}

	int countChildren = 0;
	MinimaxPlayer:OthelloDecision children[b->get_num_cols() * b->get_num_rows() - 4];
	calculateSuccessors( b, symbol, children, &countChildren );

	int bestChoice = 0;

	if ( symbol == b->get_p1_symbol() ) {
		int bestValue = INT_MIN;

		for( int i = 0; i < countChildren; i++ ) {
			int minValue = minimizingAgent( children[i].boardState, 1, 5 );
			if ( minValue > bestValue ) {
				bestValue = minValue;
				bestChoice = i;
			}
		}
	} else {
		int bestValue = INT_MAX;

		for( int i = 0; i < countChildren; i++ ) {
			int maxValue = maximizingAgent( children[i].boardState, 1, 5 );
			if ( maxValue < bestValue ) {
				bestValue = maxValue;
				bestChoice = i;
			}
		}
	}

	col = children[bestChoice].col;
	row = children[bestChoice].row;
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}

int MinimaxPlayer::maximizingAgent( OthelloBoard* board, int currentDepth, int maxDepth ) {
	if ( isGameOver( board, currentDepth, maxDepth ) ) {
		return utility(board);
	} else {
		int countChildren = 0;
		MinimaxPlayer:OthelloDecision children[board->get_num_cols() * board->get_num_rows() - 4];
		calculateSuccessors( board, board->get_p1_symbol(), children, &countChildren );

		int bestValue = INT_MIN;
		for( int i = 0; i < countChildren; i++ ) {
			int maxValue = maximizingAgent( children[i].boardState, currentDepth + 1, maxDepth );

			if ( maxValue > bestValue ) {
				bestValue = maxValue;
			}
		}

		for( int i = 0; i < countChildren; i++ ) {
			delete children[i].boardState;
		}

		return bestValue;
	}
}

int MinimaxPlayer::minimizingAgent( OthelloBoard* board, int currentDepth, int maxDepth ) {
	if ( isGameOver( board, currentDepth, maxDepth ) ) {
		return utility(board);
	} else {
		int countChildren = 0;
		MinimaxPlayer:OthelloDecision children[board->get_num_cols() * board->get_num_rows() - 4];
		calculateSuccessors( board, board->get_p2_symbol(), children, &countChildren );

		int bestValue = INT_MAX;
		for( int i = 0; i < countChildren; i++ ) {
			int maxValue = maximizingAgent( children[i].boardState, currentDepth + 1, maxDepth );

			if ( maxValue < bestValue ) {
				bestValue = maxValue;
			}
		}

		for( int i = 0; i < countChildren; i++ ) {
			delete children[i].boardState;
		}

		return bestValue;
	}
}

int MinimaxPlayer::isGameOver( OthelloBoard* board, int currentDepth, int maxDepth ) {
	if ( board->has_legal_moves_remaining(board->get_p1_symbol()) == false ) {
		if ( board->has_legal_moves_remaining(board->get_p2_symbol()) == false ) {
			return true;
		}
	}

	if ( currentDepth >= maxDepth ) {
		return true;
	}

	return false;
}

int MinimaxPlayer::utility( OthelloBoard* board ) {
	int value = board->count_score( board->get_p1_symbol() );
	value = value - board->count_score( board->get_p2_symbol() );

	return value;
}

void MinimaxPlayer::calculateSuccessors( OthelloBoard* board, char player, OthelloDecision* children, int* countChildren ) {
	if ( children == nullptr ) {
		return;
	}
	*countChildren = 0;

	for( int i = 0; i < board->get_num_rows(); i++ ) {
		for( int j = 0; j < board->get_num_cols(); j++ ) {
			if ( board->is_legal_move(j, i, player) == false ) {
				continue;
			}

			children[*countChildren].col = j;
			children[*countChildren].row = i;

			children[*countChildren].boardState = new OthelloBoard( *board );
			children[*countChildren].boardState->play_move( j, i, player );

			*countChildren += 1;
		}
	}
}
