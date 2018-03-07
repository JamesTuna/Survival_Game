import java.util.Random;

public class Obstacle {
	private Pos pos;
	int index;
	private SurvivalGame game;
	
	public Obstacle(int posx, int posy, int index, SurvivalGame game) {
		// TODO Auto-generated constructor stub
		pos = new Pos(posx, posy);
		this.index = index;
		this.game = game;
	}

	public Pos getPos() {
		return pos;
	}

	
	public void teleport() {
		Random rand;
		rand = new Random();
		// distributed at different sides
		int randx = rand.nextInt(game.D);
		int randy = game.D - randx - 1;
		while (game.positionOccupied(randx, randy)) {
			randx = rand.nextInt(game.D);
			randy = game.D - randx - 1;
		}
		pos.setPos(randx, randy);
	}
}
