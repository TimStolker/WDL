#include "hwlib.hpp"

extern "C" int odd(int a);
extern "C" int even(int a);
extern "C" int numbertohundred(int a);
extern "C" int pythagoras(int a, int b);



extern "C" void application(){

   // Test Odd:
   int num = odd(5);
   if(num == 1){
      hwlib::cout<< "Odd true PASSED \n";
   }
   else{
      hwlib::cout<< "Odd true FAILED \n";
   }

   num = odd(4);
   if(num == 0){
      hwlib::cout<< "Odd false PASSED \n";
   }
   else{
      hwlib::cout<< "Odd false FAILED \n";
   }

   // Test even:
   num = even(8);
   if(num == 1){
      hwlib::cout<< "Even true PASSED \n";
   }
   else{
      hwlib::cout<< "Even true FAILED \n";
   }

   num = even(9);
   if(num == 0){
      hwlib::cout<< "Even false PASSED \n";
   }
   else{
      hwlib::cout<< "Even false FAILED \n";
   }

   // Test numbertohundred:
   num = numbertohundred(6);
   if(num == 100){
      hwlib::cout<< "numbertohundred < 100 PASSED \n";
   }
   else{
      hwlib::cout<< "numbertohundred < 100 FAILED \n";
   }

   num = numbertohundred(105);
   if(num == 105){
      hwlib::cout<< "numbertohundred > 100 PASSED \n";
   }
   else{
      hwlib::cout<< "numbertohundred > 100 FAILED \n";
   }

   // Test pythagoras:
   num = pythagoras(5,7);
   if(num == 74){
      hwlib::cout<< "pythagoras PASSED \n";
   }
   else{
      hwlib::cout<< "pythagoras FAILED" << num << "\n";
   }
}

int main( void ){	
   
   namespace target = hwlib::target;   
    
   // wait for the PC console to start
   hwlib::wait_ms( 2000 );

   application();
}
