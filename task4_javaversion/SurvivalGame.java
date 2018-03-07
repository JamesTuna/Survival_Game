import java.util.Scanner;

public class SurvivalGame {
	private int n; // Number of player
	public final int D = 10; // dimension of board
	private final int O = 2; // Number of obstacles


	private Object[] teleportObjects;

	public static Scanner reader = new Scanner(System.in);

	public void printBoard() {
		String printObject[][] = new String[D][D];

		// init printObject
		for (int i = 0; i < D; i++)
			for (int j = 0; j < D; j++)
				printObject[i][j] = "  ";

		for (int i = 0; i < n; i++) {
			Pos pos = ((Player)teleportObjects[i]).getPos();
			printObject[pos.getX()][pos.getY()] = ((Player) teleportObjects[i]).getName();
		}

		for (int i = n; i < n+O; i++) {
			Pos pos = ((Obstacle)teleportObjects[i]).getPos();
			printObject[pos.getX()][pos.getY()] = "O" + Integer.toString(i-n);
		}

		// printing
		System.out.print(" ");
		for (int i = 0; i < D; i++)
			System.out.print(String.format("| %d  ", i));

		System.out.println("|");

		for (int i = 0; i < D * 5.5; i++)
			System.out.print("-");
		System.out.println("");

		for (int row = 0; row < D; row++) {
			System.out.print(row);
			for (int col = 0; col < D; col++)
				System.out.print(String.format("| %s ",
				printObject[row][col]));
			System.out.println("|");
			for (int i = 0; i < D * 5.5; i++)
				System.out.print("-");
			System.out.println("");
		}

	}

	public boolean positionOccupied(int randx, int randy) {
		for (Object o : teleportObjects) {
			if (o instanceof Player) {
				Pos pos = ((Player) o).getPos();
				if (pos.getX() == randx && pos.getY() == randy)
					return true;
			} else {
				Pos pos = ((Obstacle) o).getPos();
				if (pos.getX() == randx && pos.getY() == randy)
					return true;
			}
		}
		return false;
	}

	public Player getPlayer(int randx, int randy) {
		// TODO Auto-generated method stub
		for (Object o : teleportObjects) {
			if (o instanceof Player) {
				Pos pos = ((Player) o).getPos();
				if (pos.getX() == randx && pos.getY() == randy)
					return (Player) o;
			}
		}

		return null;
	}

	private  void init() {

		System.out.println("Welcome to Kafustrok. Light blesses you. \nInput number of players: (a even number)");
		n = reader.nextInt();

		teleportObjects = new Object[n + O];
		// create N/2 Humans
		for (int i = 0; i < n / 2; i++) {
			teleportObjects[i] = new Human(0, 0, i, this);
			teleportObjects[i + n / 2] = new Chark(0, 0, i, this);
		}
		// equip last one of each race with Wand
		((Human)teleportObjects[n/2-1]).equipWand();
		((Chark)teleportObjects[n-1]).equipWand();
		// create O obstacles. You cannot stand there
		for (int i = 0; i < O; i++) {
			teleportObjects[i + n] = new Obstacle(0, 0, i, this);
		}
		// positions would be reinitialized later. 0,0 is dummy
	}

	private boolean reachEnd(){
		boolean humanAllDead = true;
		boolean charkAllDead = true;
		for(int i=0;i<this.n/2;i++){
			if( ((Player)teleportObjects[i]).health > 0){
				humanAllDead = false;
				break;
			}
		}
		if(humanAllDead){
			return true;
		}
		for(int i=this.n/2;i<this.n;i++){
			if( ((Player)teleportObjects[i]).health > 0){
				charkAllDead = false;
				break;
			}
		}
		return charkAllDead;

	}

	private  void gameStart() {
		int turn = 0;
		while (!this.reachEnd()) {
			// teleport after every N turns
			if (turn == 0) {
				for (Object obj : teleportObjects) {
					if (obj instanceof Human)
						((Human) obj).teleport();
					else if (obj instanceof Chark)
						((Chark) obj).teleport();
					else if (obj instanceof Obstacle)
						((Obstacle) obj).teleport();
				}
				System.out.println("Everything gets teleported..");
			}
			printBoard();
			Player t = (Player) teleportObjects[turn];
			// t can move only if he is alive!
			if (t.health > 0) {
				// dynamic binding helps
				t.askForMove();
				System.out.println("\n");

			}
			turn = (turn + 1) % n;

		}

		System.out.println("Game over.");
		printBoard();

	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		// System.out.println(String.format("(%d,%d)", 3,4));
		SurvivalGame game = new SurvivalGame();
		game.init();
		game.gameStart();
	}
}
