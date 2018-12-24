/*********************************************************
 * config.h - Configuration data for the driver.c program.
 *********************************************************/
#ifndef _CONFIG_H_
#define _CONFIG_H_

/* 
 * CPEs for the baseline (naive) version of the rotate function that
 * was handed out to the students. Rd is the measured CPE for a dxd
 * image. Run the driver.c program on your system to get these
 * numbers.  
 */

#define R128 4.11853
#define R256 7.64520
#define R576 5.38014
#define R1024 12.49224
#define R1088 6.21969
#define R2112 7.81714

/* 
 * CPEs for the baseline (naive) version of the smooth function that
 * was handed out to the students. Sd is the measure CPE for a dxd
 * image. Run the driver.c program on your system to get these
 * numbers.  
 */

#define S32 53.40820
#define S64 53.32178
#define S128 53.31616
#define S256 53.34451
#define S576 53.36634
#define S800 53.27953

#endif /* _CONFIG_H_ */
