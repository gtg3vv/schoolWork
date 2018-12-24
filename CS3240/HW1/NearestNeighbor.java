//Gabriel Groover (gtg3vv)


import java.util.Scanner;
import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;

public class NearestNeighbor {
    
    public static void main(String[] args)
    {
        Scanner myScanner = new Scanner(System.in);
        
        System.out.print("What is the value of k? ");
        int k = Integer.parseInt(myScanner.nextLine());
        
        System.out.print("How many lines to read from the data file? ");
        int numLines = Integer.parseInt(myScanner.nextLine());
        
        Scanner input = null;
        System.out.print("File name: ");
        try{
            input = new  Scanner(new File(myScanner.nextLine()));
            
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("Failed to open file");
            System.exit(0);
        }

        ArrayList<DataPoint> dataVector = new ArrayList<DataPoint>();
    
        int i = 0;
        while (input.hasNextLine() && i < numLines)
        {
            String line = input.nextLine();
            String[] splitLine = line.split("\\s+");
            
            dataVector.add(new DataPoint(Double.parseDouble(splitLine[1]),
                                         Double.parseDouble(splitLine[2]),
                                         splitLine[0]));
            i++;          
        }
        
        System.out.print("Enter an XY pair separated by a space: ");
        double userX = myScanner.nextDouble();
        double userY = myScanner.nextDouble();
        
        while (userX != 1.0 || userY != 1.0)
        {
            calculateNeighbors(dataVector, userX, userY, k);
            System.out.print("Enter an XY pair separated by a space: ");
            userX = myScanner.nextDouble();
            userY = myScanner.nextDouble();
        }
    }
    
    private static void calculateNeighbors(ArrayList<DataPoint> dataVector, double userX, double userY, int k )
    {
        DataPoint[] neighbors = new DataPoint[k];
        Double[] distances = new Double[k];
        for (int i = 0; i < dataVector.size(); i++)
        {
            double distance = euclideanDistance(userX,userY,dataVector.get(i).getX(),dataVector.get(i).getY());
            if (i < k)
            {
                neighbors[i] = dataVector.get(i);
                neighbors[i].setDistance(distance);
            } else
            {
                for (int j = 0; j < k; j++)
                {
                    if (distance < neighbors[j].getDistance())
                    {
                        neighbors[j] = dataVector.get(i);
                        neighbors[j].setDistance(distance);
                    }
                }
            }
        }

        Arrays.sort(neighbors);
        
        double totalDist1 = 0.0;
        double totalDist2 = 0.0;
        int num1 = 0;
        int num2 = 0;
        String cat1 = neighbors[0].getCategory();
        String cat2 = "";
        for (int i = 0; i < k; i++)
        {
            System.out.println(neighbors[i].toString());
            if (neighbors[i].getCategory().equals(cat1))
            {
                totalDist1 += neighbors[i].getDistance();//distances[i];
                num1 ++;
            }
            else
            {
                cat2 = neighbors[i].getCategory();
                totalDist2 += neighbors[i].getDistance();//distances[i];
                num2++;
            }
        }
        
        if (num2 > num1)
            System.out.println("Data item (" + userX + "," + userY + ") assigned to " + cat2);
        else
            System.out.println("Data item (" + userX + "," + userY + ") assigned to " + cat1);
            
        System.out.println("Average distance to " + cat1 + " items " + totalDist1/num1);
        System.out.println("Average distance to " + cat2 + " items " + totalDist2/num2);
        
    }
    
    private static double euclideanDistance(double x1, double y1, double x2, double y2)
    {
        return Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
    }
    
}