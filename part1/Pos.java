public class Pos {
	private int x,y;

	public Pos(int x, int y) {
		// TODO Auto-generated constructor stub
		this.x = x;
		this.y = y;
	}

	public int distance(Pos another)
	{
		return Math.abs(x - another.getX()) + Math.abs(y - another.getY());
	}

	public int distance(int x1, int y1)
	{
		return Math.abs(x - x1) + Math.abs(y - y1);
	}

	public void setPos(int x, int y)
	{
		this.x = x;
		this.y = y;
	}

	public int getX() {
		return x;
	}

	public int getY() {
		return y;
	}



}
