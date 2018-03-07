public class Human extends Player {

	public Human(int posx, int posy, int index, SurvivalGame game) {
		super(80, 2, posx, posy, index, game);

		this.myString = 'H' + Integer.toString(index);
		this.equipment = new Rifle(this);

	}

	public void teleport() {
		super.teleport();
		((Rifle)this.equipment).enhance();
	}

	@Override
	public void askForMove() {
		// TODO Auto-generated method stub
		System.out.println(String.format("You are a human (H%d) using Rifle. (Range %d, Ammo #: %d, Damage per shot: %d)", this.index,
				this.equipment.getRange(),((Rifle)this.equipment).getAmmo(),
				this.equipment.getEffect() ));

		super.askForMove();

	}

}
