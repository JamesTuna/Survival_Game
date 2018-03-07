public class Chark extends Player {

	public Chark(int posx, int posy, int index, SurvivalGame game) {
		super(100, 4, posx, posy, index, game);

		this.myString = "C" + Integer.toString(index);
		this.equipment = new Axe(this);

	}

	public void teleport() {
		
		super.teleport();
		((Axe) this.equipment).enhance();
	}

	@Override
	public void askForMove() {
		// TODO Auto-generated method stub
		System.out.println(String.format("You are a Chark (C%d) using Axe. (Range: %d, Damage: %d)",this.index,
			this.equipment.getRange(), this.equipment.getEffect()));
		super.askForMove();
		
	}
}
