public abstract class Weapon {
	protected final int range;
	protected int effect;
	protected Player owner;
	
	protected Weapon(int range, int damage, Player owner) {
		this.range = range;
		this.effect = damage;
		this.owner = owner;
	}
	
	abstract public void action(int posx, int posy);
	abstract public void enhance();

	public int getEffect() {
		return this.effect;
	}

	public int getRange() {
		return this.range;
	}
}
