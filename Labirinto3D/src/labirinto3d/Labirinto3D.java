/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package labirinto3d;

import java.lang.Math;

/**
 *
 * @author 202310501
 */
public class Labirinto3D {

    
    public static final int P = 100;
    public static final int T = 50;
    public static final int S = 200;
    
    public static final int N = 10;
    public static final int[][][] labirinto = new int[N][N][N];
    
    public static void preencher() {
        
        int max = 5;
        int min = -5;
        
        
        
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                for (int k = 0; k < N; k++) { 
                    int prob = (int) (Math.random() * (10 - 1 + 1)) + 1;
                    if (prob <= 4) {
                        labirinto[i][j][k] = P;
                    }
                    else {
                        int score = (int) (Math.random() * (max - min + 1)) + min;
                        labirinto[i][j][k] = score;
                    }    
                    System.out.print(labirinto[i][j][k] + "\t");
                }
                System.out.println(" ");
            }
            System.out.println("\n\n");
        }
        
//        int i = (int) (Math.random() * ((N-1) - 0 + 1)) + 0;
//        int j = (int) (Math.random() * ((N-1) - 0 + 1)) + 0;
//        int k = (int) (Math.random() * ((N-1) - 0 + 1)) + 0;
        
        
        
    }
    
    
    public static void main(String[] args) {
        // TODO code application logic here
        preencher();
    }
    
}
