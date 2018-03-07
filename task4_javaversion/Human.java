public class Human extends Player {

	public Human(int posx, int posy, int index, SurvivalGame game) {
		super(80, 2, posx, posy, index, game);

		this.myString = 'H' + Integer.toString(index);
		this.equipment = new Rifle(this);

	}

	public void equipWand(){
		this.equipment = new Wand(this);
	}

	public void teleport() {
		super.teleport();
		if(this.equipment instanceof Rifle){
			((Rifle)this.equipment).enhance();
		}else if(this.equipment instanceof Wand){
			((Wand)this.equipment).enhance();
		}
	}


	@Override
	public void askForMove() {
		// TODO Auto-generated method stub
		if(this.equipment instanceof Rifle){
			System.out.println(String.format("You are a human (H%d) using Rifle. (Range %d, Ammo #: %d, Damage per shot: %d)", this.index,
					((Weapon)this.equipment).getRange(),((Rifle)this.equipment).getAmmo(),
					((Weapon)this.equipment).getEffect() ));

			super.askForMove();
		}
		else if(this.equipment instanceof Wand){
			System.out.println(String.format("You are a human (H%d) using Wand. (Range %d, Effect: %d)", this.index,
					((Wand)this.equipment).getRange(),((Wand)this.equipment).getEffect() ));

			super.askLast();
		}
	}

}
