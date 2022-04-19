using System;
public class Program {
    public static void Main() {
int [] data = {100,9000,500,6000};
int [] result = {0,0,0,0};
int i = 0;
while ( i < 4 ) 
 {
 int a = data[i];
int b = data[i];
if ( a > 0 ) 
 { 
 while ( b > 0 ) 
 {
 if ( a > b ) 
 { 
 a = a - b;
 
 }
if ( !(a > b) ) 
 { 
 b = b - a;
 
 }
 
}
 
 }
result[i] = a;
i = i + 1;
 
}
Console.WriteLine(result[1]);
}
}