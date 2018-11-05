#ifndef RANDOM_PLAYER
#define RANDOM_PLAYER

#include "Player.h"
#include "OthelloBoard.h"

/**
 * This class represents a human player
 */
class RandomPlayer : public Player {
public:

	/**
	 * @symb The symbol used for the human player's pieces
	 * The constructor for the HumanPlayer class
	 */
    RandomPlayer(char symb);

    /**
     * Destructor
     */
    virtual ~RandomPlayer();

    /**
     * @param b The current board for the game.
     * @param col Holds the return value for the column of the move
     * @param row Holds the return value for the row of the move
     * Obtains the (col,row) coordinates for the current move
     */
    void get_move(OthelloBoard* b, int& col, int& row);

    /**
     * @return A pointer to a copy of the HumanPlayer object
     * This is a virtual copy constructor
     */
    RandomPlayer *clone();
private:

};

#endif
