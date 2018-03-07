public class Wand{
    private static final int WAND_RANGE = 5;
    private static final int WAND_INIT_EFFECT = 5;
    protected final int range;
  	protected int effect;
  	protected Player owner;

    public Wand(Player owner){
        this.range = WAND_RANGE;
        this.effect = WAND_INIT_EFFECT;
        this.owner = owner;
    }
    public void enhance(){
        this.effect+=5;
    }
    public int getEffect(){
        return this.effect;
    }
    public int getRange(){
        return this.range;
    }
    public void action(int posx,int posy){
        System.out.println("You are using wand healing " + posx + " " + posy + ".");
        if (this.owner.pos.distance(posx,posy) <= this.range){
            Player player = this.owner.game.getPlayer(posx, posy);
            if (player == null){
                System.out.println("You heal nothing");
            }
            else if(!this.owner.getClass().isInstance(player) ){
                System.out.println("You cannot heal your opponent!");
            }
            else if(this.owner.getClass().isInstance(player) ){
                player.increaseHealth(this.effect);
            }
        }
        else{
            System.out.println("Out of reach.");
        }
        return;
    }
}
