#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <cstring>
#include <cstdlib>

using namespace cv;
using namespace std;


void inject(char* message, Mat& mat);
char* extract(const Mat& mat);

int main(int argc, char** argv )
{
    
    if(argc < 2)
    {
        cout << "Command line args not specified...\n(format 1)\n" ;
        cout << "$ ./stego <file1>\n" ;
        cout << "\tExtract the message hidden inside image specified by file1\n(format 2)\n" ;
        cout << "$ ./stego <file1> <file2>\n" ;
        cout << "\tRead file1 and store a message inside. Copy to file2\n" ;
        return(-1);
    }

    Mat img;
    img = imread(argv[1], CV_LOAD_IMAGE_COLOR);

    if(! img.data )                              // Check for invalid input
    {
        cout <<  "Could not open or find the image" << std::endl ;
        return -1;
    }
    
    if(argc == 2)
    {
        char* message = extract(img);
        cout << message << '\n' ;
    }

    else if(argc >= 3)
    {
        char text[1024];
        cout << "enter a string: " ;
        cin.get(text, (img.rows* img.cols)/2) ;

    
        inject(text, img);                      // inject message into carrier file

        /*
        namedWindow( "new", WINDOW_AUTOSIZE );      // display modified image
        imshow( "new", img);               
        */

        vector<int> params;
        params.push_back(CV_IMWRITE_PNG_COMPRESSION);
        params.push_back(9);
        imwrite(argv[2], img, params);

        waitKey(0);                      // Wait for a keystroke in the window
    }

    
    return 0;
}

void inject(char* message, Mat& mat)
{
    unsigned char bits, temp;
    unsigned char mask[2] = {240, 15};

    for(int i=0; i < strlen(message) + 1; i++)
    {
        for(int j=0; j < 2; j++)
        {
            bits = message[i] & mask[j];
            bits = bits >> 4*(1 - j);
            temp = mat.data[2*i + j];
            temp = temp - temp%16;
            mat.data[2*i +j] = temp + bits;
        }
    }
}

char* extract(const Mat& mat)
{
    unsigned char mask = 15;
    unsigned char c;
    char buffer[1024];

    for(int i=0; i <2048 ; i++)
    { 
        if(i%2 == 0)
            c = (mask & mat.data[i]) << 4 ;
        else
        {
            c += mask & mat.data[i] ;
            buffer[i/2] = c;
            if(c == 0)
            break;
        }
    }

    return(strdup(buffer));
}
