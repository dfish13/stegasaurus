#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <cstring>
#include <cstdlib>

using namespace cv;
using namespace std;


void inject(char* message, Mat& carrier);
void inject(const Mat& img, Mat& carrier);
char* extract(const Mat& carrier);

int main(int argc, char** argv )
{
    
    if(argc < 2)
    {
        cout << "Command line args not specified...\n(format 1)\n" ;
        cout << "$ ./stego <file1>\n" ;
        cout << "\tExtract the message hidden inside image specified by <file1>\n(format 2)\n" ;
        cout << "$ ./stego <file1> <file2>\n" ;
        cout << "\tRead <file1> and store a message inside. Copy to <file2>\n(format 3)\n" ;
        cout << "$ ./stego <file1> <file2> <file3>\n" ;
        cout << "\tRead <file1> and store <file2> inside. Copy to <file3>\n" ;
        return(-1);
    }

    Mat carrier = imread(argv[1], CV_LOAD_IMAGE_COLOR);

    if(! carrier.data )                              // Check for invalid input
    {
        cout <<  "Could not open <file1>" << std::endl ;
        return(-1);
    }
    cout << "old\n" << carrier ;
    
    if(argc == 2)
    {
        char* message = extract(carrier);
        cout << message << '\n' ;
        return 0;
    }

    else if(argc == 3)
    {
        char text[1024];
        cout << "enter a string: " ;
        cin.get(text, (carrier.rows* carrier.cols)/2) ;

    
        inject(text, carrier);                      // inject message into carrier file
    }
    else if(argc == 4)
    {
        Mat img = imread(argv[2], CV_LOAD_IMAGE_GRAYSCALE);
        if(! carrier.data )
        {
            cout <<  "Could not open <file1>" << std::endl ;
            return(-1);
        }

        inject(img, carrier);
    }

    vector<int> params;     
    params.push_back(CV_IMWRITE_PNG_COMPRESSION);   // specify the type of image to save as (PNG)
    params.push_back(9);
    imwrite(argv[argc-1], carrier, params);

    cout << "new\n" << carrier ;


    
    return 0;
}

/*
    injects ascii text from message into the carrier image.
*/
void inject(char* message, Mat& carrier)
{
    unsigned char bits, temp;
    unsigned char mask[2] = {240, 15};

    for(int i=0; i < strlen(message) + 1; i++)
    {
        for(int j=0; j < 2; j++)
        {
            bits = message[i] & mask[j];
            bits = bits >> 4*(1 - j);
            temp = carrier.data[2*i + j];
            temp = temp - temp%16;
            carrier.data[2*i +j] = temp + bits;
        }
    }
}

/*
    injects the bytes of img inside carrier at a ratio of 2 to 1.
*/
void inject(const Mat& img, Mat& carrier)
{
    unsigned char bits, temp;
    unsigned char mask[2] = {240, 15};
    int img_size = img.channels() * img.rows * img.cols ;
    int carrier_size = carrier.channels() * carrier.rows * carrier.cols ;

    if( 2*img_size > carrier_size)
    {
        cout << "<file1> not large enough to hold <file2>\n" ;
        return;
    }

    for(int i=0; i < img_size; i++)
    {
        for(int j=0; j<2; j++)
        {
            bits = img.data[i] & mask[j];
            bits = bits >> 4*(1 - j);
            temp = carrier.data[2*i + j];
            temp = temp - temp%16;
            carrier.data[2*i +j] = temp + bits;
        }
    }
}

/*
    extracts ascii text from carrier.
    stops when a null character is encountered.
*/
char* extract(const Mat& carrier)
{
    unsigned char c, mask = 15;
    char buffer[1024];

    for(int i=0; i <2048 ; i++)
    { 
        if(i%2 == 0)
            c = (mask & carrier.data[i]) << 4 ;
        else
        {
            c += mask & carrier.data[i] ;
            buffer[i/2] = c;
            if(c == 0)
            break;
        }
    }
    return(strdup(buffer));
}
