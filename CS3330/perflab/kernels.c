/********************************************************
 * Kernels to be optimized for the CS:APP Performance Lab
 ********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "defs.h"

/* 
 * Please fill in the following team struct 
 */
team_t team = {
    "FredRick",              /* Team name */

    "Gabriel T. Groover",     /* First member full name */
    "gtg3vv@virginia.edu",  /* First member email address */

    "Haitian Xie",                   /* Second member full name (leave blank if none) */
    "hx8rc@virginia.edu"                    /* Second member email addr (leave blank if none) */
};

/***************
 * ROTATE KERNEL
 ***************/

/******************************************************
 * Your different versions of the rotate kernel go here
 ******************************************************/

/* 
 * naive_rotate - The naive baseline version of rotate 
 */
char naive_rotate_descr[] = "naive_rotate: Naive baseline implementation";
void naive_rotate(int dim, pixel *src, pixel *dst) 
{
    int i, j;

    for (i = 0; i < dim; i++)
	for (j = 0; j < dim; j++)
	    dst[RIDX(dim-1-j, i, dim)] = src[RIDX(i, j, dim)];
}

/* 
 * rotate - Another version of rotate
 */
char rotate_descr[] = "rotate: Current working version";
void rotate(int dim, pixel *src, pixel *dst) 
{
    naive_rotate(dim, src, dst);
}

/*********************************************************************
 * register_rotate_functions - Register all of your different versions
 *     of the rotate kernel with the driver by calling the
 *     add_rotate_function() for each test function. When you run the
 *     driver program, it will test and report the performance of each
 *     registered test function.  
 *********************************************************************/

void register_rotate_functions() 
{
   // add_rotate_function(&naive_rotate, naive_rotate_descr);   
   // add_rotate_function(&rotate, rotate_descr);   
    /* ... Register additional test functions here */
}


/***************
 * SMOOTH KERNEL
 **************/

/***************************************************************
 * Various typedefs and helper functions for the smooth function
 * You may modify these any way you like.
 **************************************************************/

/* A struct used to compute averaged pixel value */
typedef struct {
    int red;
    int green;
    int blue;
    int num;
} pixel_sum;

/* Compute min and max of two integers, respectively */
static int min(int a, int b) { return (a < b ? a : b); }
static int max(int a, int b) { return (a > b ? a : b); }

/* 
 * initialize_pixel_sum - Initializes all fields of sum to 0 
 */
static void initialize_pixel_sum(pixel_sum *sum) 
{
    sum->red = sum->green = sum->blue = 0;
    sum->num = 0;
    return;
}

/* 
 * accumulate_sum - Accumulates field values of p in corresponding 
 * fields of sum 
 */
static void accumulate_sum(pixel_sum *sum, pixel p) 
{
    sum->red += (int) p.red;
    sum->green += (int) p.green;
    sum->blue += (int) p.blue;
    sum->num++;
    return;
}

/* 
 * assign_sum_to_pixel - Computes averaged pixel value in current_pixel 
 */
static void assign_sum_to_pixel(pixel *current_pixel, pixel_sum sum,int i,int j,int dim) 
{
    // if ((i == j && j == 0) || (i == dim-1 && j == 0) || (i == 0 && j == dim-1) || (i == j && j == dim-1))
    // {
    //     current_pixel->red = (unsigned short) (sum.red/4);
    //     current_pixel->green = (unsigned short) (sum.green/4);
    //     current_pixel->blue = (unsigned short) (sum.blue/4);
    // }else if (i == 0 || j == 0 || i == dim-1 || j == dim-1)
    // {
    //     current_pixel->red = (unsigned short) (sum.red/6);
    //     current_pixel->green = (unsigned short) (sum.green/6);
    //     current_pixel->blue = (unsigned short) (sum.blue/6);
    // } else
    // {
    //     current_pixel->red = (unsigned short) (sum.red/9);
    //     current_pixel->green = (unsigned short) (sum.green/9);
    //     current_pixel->blue = (unsigned short) (sum.blue/9);
    // }
        current_pixel->red = (unsigned short) (sum.red/sum.num);
         current_pixel->green = (unsigned short) (sum.green/sum.num);
         current_pixel->blue = (unsigned short) (sum.blue/sum.num);

    return;
}

/* 
 * avg - Returns averaged pixel value at (i,j) 
 */
static pixel avg(int dim, int i, int j, pixel *src) 
{
    int ii, jj;
    pixel_sum sum;
    pixel current_pixel;

    initialize_pixel_sum(&sum);
    for(ii = max(i-1, 0); ii <= min(i+1, dim-1); ii++) 
	for(jj = max(j-1, 0); jj <= min(j+1, dim-1); jj++) 
	    accumulate_sum(&sum, src[RIDX(ii, jj, dim)]);

    assign_sum_to_pixel(&current_pixel, sum,i,j,dim);
    return current_pixel;
}

/******************************************************
 * Your different versions of the smooth kernel go here
 ******************************************************/

/*
 * naive_smooth - The naive baseline version of smooth 
 */
char naive_smooth_descr[] = "naive_smooth: Naive baseline implementation";
void naive_smooth(int dim, pixel *src, pixel *dst) 
{
    int i, j;

    for (i = 0; i < dim; i++)
	for (j = 0; j < dim; j++)
	    dst[RIDX(i, j, dim)] = avg(dim, i, j, src);
}

/*
 * smooth - Another version of smooth. 
 */
char smooth_descr[] = "smooth: Current working version";
void smooth(int dim, pixel *src, pixel *dst) 
{
    naive_smooth(dim, src, dst);
}

char opt_smooth_descr[] = "smooth: separate each of the cases for averaging a pixel and inline most functions";
void opt_smooth(int dim, pixel *src, pixel *dst)
{
    //pixel_sum sum->red = sum->green = sum->blue = 0;
    int red,blue,green;
    red=blue=green=0;
    
    //Upper left
    red += src[RIDX(0,0,dim)].red;
    green +=  src[RIDX(0,0,dim)].green;
    blue +=  src[RIDX(0,0,dim)].blue;
    red += src[RIDX(1,0,dim)].red;
    green +=  src[RIDX(1,0,dim)].green;
    blue +=  src[RIDX(1,0,dim)].blue;
    red += src[RIDX(1,1,dim)].red;
    green +=  src[RIDX(1,1,dim)].green;
    blue +=  src[RIDX(1,1,dim)].blue;
    red += src[RIDX(0,1,dim)].red;
    green +=  src[RIDX(0,1,dim)].green;
    blue +=  src[RIDX(0,1,dim)].blue;
    
    pixel p;
    p.red = red/4;
    p.blue = blue/4;
    p.green = green/4;
    dst[RIDX(0,0,dim)] = p;
    
    //upper right
    red = blue = green = 0;
    red += src[RIDX(0,dim-1,dim)].red;
    green +=  src[RIDX(0,dim-1,dim)].green;
    blue +=  src[RIDX(0,dim-1,dim)].blue;
    red += src[RIDX(0,dim-2,dim)].red;
    green +=  src[RIDX(0,dim-2,dim)].green;
    blue +=  src[RIDX(0,dim-2,dim)].blue;
    red += src[RIDX(1,dim-2,dim)].red;
    green +=  src[RIDX(1,dim-2,dim)].green;
    blue +=  src[RIDX(1,dim-2,dim)].blue;
    red += src[RIDX(1,dim-1,dim)].red;
    green +=  src[RIDX(1,dim-1,dim)].green;
    blue +=  src[RIDX(1,dim-1,dim)].blue;
    
    //pixel p;
    p.red = red/4;
    p.blue = blue/4;
    p.green = green/4;
    dst[RIDX(0,dim-1,dim)] = p;
    
    //bottom left
    red = blue = green = 0;
    red += src[RIDX(dim-1,0,dim)].red;
    green +=  src[RIDX(dim-1,0,dim)].green;
    blue +=  src[RIDX(dim-1,0,dim)].blue;
    red += src[RIDX(dim-1,1,dim)].red;
    green +=  src[RIDX(dim-1,1,dim)].green;
    blue +=  src[RIDX(dim-1,1,dim)].blue;
    red += src[RIDX(dim-2,0,dim)].red;
    green +=  src[RIDX(dim-2,0,dim)].green;
    blue +=  src[RIDX(dim-2,0,dim)].blue;
    red += src[RIDX(dim-2,1,dim)].red;
    green +=  src[RIDX(dim-2,1,dim)].green;
    blue +=  src[RIDX(dim-2,1,dim)].blue;
    
    //pixel p;
    p.red = red/4;
    p.blue = blue/4;
    p.green = green/4;
    dst[RIDX(dim-1,0,dim)] = p;
    
      //bottom right
    red = blue = green = 0;
    red += src[RIDX(dim-2,dim-2,dim)].red;
    green +=  src[RIDX(dim-2,dim-2,dim)].green;
    blue +=  src[RIDX(dim-2,dim-2,dim)].blue;
    red += src[RIDX(dim-1,dim-1,dim)].red;
    green +=  src[RIDX(dim-1,dim-1,dim)].green;
    blue +=  src[RIDX(dim-1,dim-1,dim)].blue;
    red += src[RIDX(dim-2,dim-1,dim)].red;
    green +=  src[RIDX(dim-2,dim-1,dim)].green;
    blue +=  src[RIDX(dim-2,dim-1,dim)].blue;
    red += src[RIDX(dim-1,dim-2,dim)].red;
    green +=  src[RIDX(dim-1,dim-2,dim)].green;
    blue +=  src[RIDX(dim-1,dim-2,dim)].blue;
    
   // pixel p;
    p.red = red/4;
    p.blue = blue/4;
    p.green = green/4;
    dst[RIDX(dim-1,dim-1,dim)] = p;
    
    //left side
    int i;
    for (i = 1; i < dim-1; i++)
    {
        //pixel p;
        red = blue = green = 0;
        
        red += src[RIDX(i-1,0,dim)].red;
        green +=  src[RIDX(i-1,0,dim)].green;
        blue +=  src[RIDX(i-1,0,dim)].blue;
        red += src[RIDX(i-1,1,dim)].red;
        green +=  src[RIDX(i-1,1,dim)].green;
        blue +=  src[RIDX(i-1,1,dim)].blue;
        red += src[RIDX(i,0,dim)].red;
        green +=  src[RIDX(i,0,dim)].green;
        blue +=  src[RIDX(i,0,dim)].blue;
        red += src[RIDX(i,1,dim)].red;
        green +=  src[RIDX(i,1,dim)].green;
        blue +=  src[RIDX(i,1,dim)].blue;
        red += src[RIDX(i+1,0,dim)].red;
        green +=  src[RIDX(i+1,0,dim)].green;
        blue +=  src[RIDX(i+1,0,dim)].blue;
        red += src[RIDX(i+1,1,dim)].red;
        green +=  src[RIDX(i+1,1,dim)].green;
        blue +=  src[RIDX(i+1,1,dim)].blue;
        
        p.red = red/6;
        p.blue = blue/6;
        p.green = green/6;
        dst[RIDX(i,0,dim)] = p;
    }
    //right
    for (i = 1; i < dim-1; i++)
    {
        //pixel p;
        red = blue = green = 0;
        
        red += src[RIDX(i-1,dim-2,dim)].red;
        green +=  src[RIDX(i-1,dim-2,dim)].green;
        blue +=  src[RIDX(i-1,dim-2,dim)].blue;
        red += src[RIDX(i-1,dim-1,dim)].red;
        green +=  src[RIDX(i-1,dim-1,dim)].green;
        blue +=  src[RIDX(i-1,dim-1,dim)].blue;
        red += src[RIDX(i,dim-2,dim)].red;
        green +=  src[RIDX(i,dim-2,dim)].green;
        blue +=  src[RIDX(i,dim-2,dim)].blue;
        red += src[RIDX(i,dim-1,dim)].red;
        green +=  src[RIDX(i,dim-1,dim)].green;
        blue +=  src[RIDX(i,dim-1,dim)].blue;
        red += src[RIDX(i+1,dim-2,dim)].red;
        green +=  src[RIDX(i+1,dim-2,dim)].green;
        blue +=  src[RIDX(i+1,dim-2,dim)].blue;
        red += src[RIDX(i+1,dim-1,dim)].red;
        green +=  src[RIDX(i+1,dim-1,dim)].green;
        blue +=  src[RIDX(i+1,dim-1,dim)].blue;
        
        p.red = red/6;
        p.blue = blue/6;
        p.green = green/6;
        dst[RIDX(i,dim-1,dim)] = p;
    }
    //top edge
    int j;
    for (j = 1; j < dim-1; j++)
    {
        //pixel p;
        red = blue = green = 0;
        
        red += src[RIDX(0,j-1,dim)].red;
        green +=  src[RIDX(0,j-1,dim)].green;
        blue +=  src[RIDX(0,j-1,dim)].blue;
        red += src[RIDX(0,j,dim)].red;
        green +=  src[RIDX(0,j,dim)].green;
        blue +=  src[RIDX(0,j,dim)].blue;
        red += src[RIDX(0,j+1,dim)].red;
        green +=  src[RIDX(0,j+1,dim)].green;
        blue +=  src[RIDX(0,j+1,dim)].blue;
        red += src[RIDX(1,j-1,dim)].red;
        green +=  src[RIDX(1,j-1,dim)].green;
        blue +=  src[RIDX(1,j-1,dim)].blue;
        red += src[RIDX(1,j,dim)].red;
        green +=  src[RIDX(1,j,dim)].green;
        blue +=  src[RIDX(1,j,dim)].blue;
        red += src[RIDX(1,j+1,dim)].red;
        green +=  src[RIDX(1,j+1,dim)].green;
        blue +=  src[RIDX(1,j+1,dim)].blue;
        
        p.red = red/6;
        p.blue = blue/6;
        p.green = green/6;
        dst[RIDX(0,j,dim)] = p;
    }
    //bottom edge
    for (j = 1; j < dim-1; j++)
    {
        //pixel p;
        red = blue = green = 0;
        
        red += src[RIDX(dim-1,j-1,dim)].red;
        green +=  src[RIDX(dim-1,j-1,dim)].green;
        blue +=  src[RIDX(dim-1,j-1,dim)].blue;
        red += src[RIDX(dim-1,j,dim)].red;
        green +=  src[RIDX(dim-1,j,dim)].green;
        blue +=  src[RIDX(dim-1,j,dim)].blue;
        red += src[RIDX(dim-1,j+1,dim)].red;
        green +=  src[RIDX(dim-1,j+1,dim)].green;
        blue +=  src[RIDX(dim-1,j+1,dim)].blue;
        red += src[RIDX(dim-2,j-1,dim)].red;
        green +=  src[RIDX(dim-2,j-1,dim)].green;
        blue +=  src[RIDX(dim-2,j-1,dim)].blue;
        red += src[RIDX(dim-2,j,dim)].red;
        green +=  src[RIDX(dim-2,j,dim)].green;
        blue +=  src[RIDX(dim-2,j,dim)].blue;
        red += src[RIDX(dim-2,j+1,dim)].red;
        green +=  src[RIDX(dim-2,j+1,dim)].green;
        blue +=  src[RIDX(dim-2,j+1,dim)].blue;
        
        p.red = red/6;
        p.blue = blue/6;
        p.green = green/6;
        dst[RIDX(dim-1,j,dim)] = p;
    }
    //middle part
    for(i=1;i<dim-1;i++){
        for(j=1;j<dim-1;j++){
           // pixel p;
            red = blue = green = 0;
            //i-1
            red += src[RIDX(i-1,j-1,dim)].red;
            green +=  src[RIDX(i-1,j-1,dim)].green;
            blue +=  src[RIDX(i-1,j-1,dim)].blue;
            red += src[RIDX(i-1,j,dim)].red;
            green +=  src[RIDX(i-1,j,dim)].green;
            blue +=  src[RIDX(i-1,j,dim)].blue;
            red += src[RIDX(i-1,j+1,dim)].red;
            green +=  src[RIDX(i-1,j+1,dim)].green;
            blue +=  src[RIDX(i-1,j+1,dim)].blue;
            //i
            red += src[RIDX(i,j-1,dim)].red;
            green +=  src[RIDX(i,j-1,dim)].green;
            blue +=  src[RIDX(i,j-1,dim)].blue;
            red += src[RIDX(i,j,dim)].red;
            green +=  src[RIDX(i,j,dim)].green;
            blue +=  src[RIDX(i,j,dim)].blue;
            red += src[RIDX(i,j+1,dim)].red;
            green +=  src[RIDX(i,j+1,dim)].green;
            blue +=  src[RIDX(i,j+1,dim)].blue;
            //i+1
            red += src[RIDX(i+1,j-1,dim)].red;
            green +=  src[RIDX(i+1,j-1,dim)].green;
            blue +=  src[RIDX(i+1,j-1,dim)].blue;
            red += src[RIDX(i+1,j,dim)].red;
            green +=  src[RIDX(i+1,j,dim)].green;
            blue +=  src[RIDX(i+1,j,dim)].blue;
            red += src[RIDX(i+1,j+1,dim)].red;
            green +=  src[RIDX(i+1,j+1,dim)].green;
            blue +=  src[RIDX(i+1,j+1,dim)].blue;
            
            p.red = red/9;
            p.blue = blue/9;
            p.green = green/9;
            dst[RIDX(i,j,dim)] = p;
        }
    }
    
    
    
    
    
}

/********************************************************************* 
 * register_smooth_functions - Register all of your different versions
 *     of the smooth kernel with the driver by calling the
 *     add_smooth_function() for each test function.  When you run the
 *     driver program, it will test and report the performance of each
 *     registered test function.  
 *********************************************************************/

void register_smooth_functions() {
    //add_smooth_function(&smooth, smooth_descr);
    add_smooth_function(&naive_smooth, naive_smooth_descr);
    add_smooth_function(&opt_smooth, opt_smooth_descr);
    /* ... Register additional test functions here */
}

