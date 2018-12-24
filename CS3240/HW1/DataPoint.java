public class DataPoint implements Comparable<DataPoint> {

    private double x;
    private double y;
    private double distance;
    private String category;
    
    public DataPoint()
    {
        this.x = 0;
        this.y = 0;
        this.distance = 0;
        this.category = "";
    }
    
    public  DataPoint(double x, double y, String category)
    {
        this.x = x;
        this.y = y; 
        this.category = category;
        this.distance = 0;
    }
    
    public double getX()
    {
        return this.x;
    }
    
    public double getY()
    {
        return this.y;
    }
    
    public String getCategory()
    {
        return this.category;
    }
    
    public double getDistance()
    {
        return distance;
    }
    
    public void setDistance(double distance)
    {
        this.distance = distance;
    }
    
    public int compareTo(DataPoint other)
    {
        if (this.distance > other.getDistance())
            return 1;
        return -1;
    }
    
    public String toString()
    {
        return this.category + " " + this.x + " " + this.y + " " + this.distance;
    }

}
