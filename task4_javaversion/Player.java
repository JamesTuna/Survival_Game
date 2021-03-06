import java.util.Random;

public abstract class Player {
	private int MOBILITY;
	private int HEALTH_CAP;
	protected Pos pos;
	protected int health;
	protected Object equipment;
	protected int index;
	protected String myString;
	protected SurvivalGame game;


	public Player(int healthCap, int mob, int posx, int posy, int index, SurvivalGame game) {
		this.HEALTH_CAP = healthCap;
		this.MOBILITY = mob;
		this.health = healthCap;
		this.pos = new Pos(posx, posy);
		this.index = index;
		this.game = game;
	}

	public Pos getPos() {
		return pos;
	}

	public void teleport() {

		Random rand;
		rand = new Random();
		int randx = rand.nextInt(game.D);
		int randy = rand.nextInt(game.D);
		while (game.positionOccupied(randx, randy)) {
			randx = rand.nextInt(game.D);
			randy = rand.nextInt(game.D);
		}
		pos.setPos(randx, randy);
	}

	public void increaseHealth(int h) {
		boolean dead = false;
		if(this.health <= 0){
			dead = true;
		}
		int after = this.health+h;
		if(after<=this.HEALTH_CAP){
			this.health = after;
		}
		else{
			this.health = this.HEALTH_CAP;
		}
		if(this.health>0 && dead==true){
			this.myString = this.myString.charAt(1)+Integer.toString(this.index);
		}
		return ;
	}

	public void decreaseHealth(int h) {
		this.health -= h;
		if (this.health <= 0)
			this.myString = "C" + this.myString.charAt(0);
	}

	public String getName() {
		return myString;
	}

	public void askForMove() {
		// Print general information
		System.out.println("Your health is " + health
				+ String.format(". Your position is (%d,%d). Your mobility is %d.", pos.getX(), pos.getY(), this.MOBILITY));

		System.out.println("You now have following options: ");
		System.out.println("1. Move");
		System.out.println("2. Attack");
		System.out.println("3. End tne turn");

		int a = SurvivalGame.reader.nextInt();

		if (a == 1) {
			System.out.println("Specify your target position (Input 'x y').");
			int posx = SurvivalGame.reader.nextInt(), posy = SurvivalGame.reader.nextInt();
			if (pos.distance(posx, posy) > this.MOBILITY) {
				System.out.println("Beyond your reach. Staying still.");
			} else if (game.positionOccupied(posx, posy)) {
				System.out.println("Position occupied. Cannot move there.");
			} else {
				this.pos.setPos(posx, posy);
				game.printBoard();
				System.out.println("You can now \n1.attack\n2.End the turn");
				if (SurvivalGame.reader.nextInt() == 1) {
					System.out.println("Input position to attack. (Input 'x y')");
					int attx = SurvivalGame.reader.nextInt(), atty = SurvivalGame.reader.nextInt();
					// determine class of equipment: by default in askForMove, it must be of class weapon
					((Weapon)this.equipment).action(attx, atty);
				}
			}
		} else if (a == 2) {
			System.out.println("Input position to attack.");
			int attx = SurvivalGame.reader.nextInt(), atty = SurvivalGame.reader.nextInt();
			// determine class of equipment: by default in askForMove, it must be of class weapon
			((Weapon)this.equipment).action(attx, atty);
		} else if (a == 3) {
			return;
		}
	}
	// ask instructions for Player with a Wand
	public void askLast() {
		// Print general information
		System.out.println("Your health is " + health
				+ String.format(". Your position is (%d,%d). Your mobility is %d.", pos.getX(), pos.getY(), this.MOBILITY));

		System.out.println("You now have following options: ");
		System.out.println("1. Move");
		System.out.println("2. Heal");
		System.out.println("3. End tne turn");

		int a = SurvivalGame.reader.nextInt();

		if (a == 1) {
			System.out.println("Specify your target position (Input 'x y').");
			int posx = SurvivalGame.reader.nextInt(), posy = SurvivalGame.reader.nextInt();
			if (pos.distance(posx, posy) > this.MOBILITY) {
				System.out.println("Beyond your reach. Staying still.");
			} else if (game.positionOccupied(posx, posy)) {
				System.out.println("Position occupied. Cannot move there.");
			} else {
				this.pos.setPos(posx, posy);
				game.printBoard();
				System.out.println("You can now \n1.heal\n2.End the turn");
				if (SurvivalGame.reader.nextInt() == 1) {
					System.out.println("Input position to heal. (Input 'x y')");
					int attx = SurvivalGame.reader.nextInt(), atty = SurvivalGame.reader.nextInt();
					// determine the class for equipment, by default in askLast() it is of class Wand
					((Wand)this.equipment).action(attx, atty);
				}
			}
		} else if (a == 2) {
			System.out.println("Input position to heal.");
			int attx = SurvivalGame.reader.nextInt(), atty = SurvivalGame.reader.nextInt();
			// determine the class for equipment, by default in askLast() it is of class Wand
			((Wand)this.equipment).action(attx, atty);
		} else if (a == 3) {
			return;
		}
	}

}
