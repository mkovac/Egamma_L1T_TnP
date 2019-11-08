#include "RooMath.h"
#include "TMath.h"
#include <math.h>

Double_t ApproxErf(Double_t arg) 
{
  static const double erflim = 5.0;
  if( arg > erflim )
    return 1.0;
  if( arg < -erflim )
    return -1.0;
  
  return RooMath::erf(arg);
}

Double_t myfunction(double *x, double *p) 
{ 
   const double sqrtPiOver2 = 1.2533141373; // sqrt(pi/2)
   const double sqrt2 = 1.4142135624;

   double m=x[0];
   double m0=p[0];
   double sigma=p[1];
   double alpha=p[2];
   double n= p[3];
   double norm=p[4];

   Double_t sig = fabs((Double_t) sigma);
   
   Double_t t = (m - m0)/sig ;
   
   if (alpha < 0)
     t = -t;

   Double_t absAlpha = fabs(alpha / sig);
   Double_t a = TMath::Power(n/absAlpha,n)*exp(-0.5*absAlpha*absAlpha);
   Double_t b = absAlpha - n/absAlpha;

   Double_t aireGauche = (1 + ApproxErf( absAlpha / sqrt2 )) * sqrtPiOver2 ;
   Double_t aireDroite = ( a * 1/TMath::Power(absAlpha - b,n-1)) / (n - 1);
   Double_t aire = aireGauche + aireDroite;

   if ( t <= absAlpha ){
     return norm * (1 + ApproxErf( t / sqrt2 )) * sqrtPiOver2 / aire ;
   }
   else{
     return norm * (aireGauche +  a * (1/TMath::Power(t-b,n-1) - 1/TMath::Power(absAlpha - b,n-1)) / (1 - n)) / aire ;
   }
  
 } 

