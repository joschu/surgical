#include <stdlib.h>

#ifdef MAC
#include <OpenGL/gl.h>
#include <GLUT/glut.h>
#include <GL/gle.h>
#else
#include <GL/gl.h>
#include <GL/glut.h>
#include <GL/gle.h>
#endif

#include <iostream>
#include <fstream>

#include <Eigen/Core>
#include <Eigen/Geometry>
#include <math.h>
#include "thread_discrete.h"
#include "trajectory_reader.h"
#include "glThread.h"
#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <opencv/cxcore.h>


#ifdef ISOTROPIC

//#define TRAJ_BASE_NAME "./LearnParams/config/suturenylon_processed_projected"
#define TRAJ_BASE_NAME "./LearnParams/config/suturepurple_processed_projected"
//#define TRAJ_BASE_NAME "./LearnParams/config/sutureblack_processed_projected"

#else
#define TRAJ_BASE_NAME "./LearnParams/config/ribbon_dots_processed_projected"
#endif


#define IMG_SAVE_OPENGL "savedIms/opengl_"



// import most common Eigen types
USING_PART_OF_NAMESPACE_EIGEN
using namespace cv;


void InitLights();
void InitGLUT(int argc, char * argv[]);
void InitStuff();
void DrawStuff();
void DrawAxes();
void InitThread(int argc, char* argv[]);
void save_opengl_image();
void update_all_threads();




#define NUM_PTS 500
// #define THREAD_RADII 1.0
#define MOVE_POS_CONST 1.0
#define MOVE_TAN_CONST 0.2
#define ROTATE_TAN_CONST 0.2

#define PIX_WIDTH 1200
#define PIX_HEIGHT 1200


enum key_code {NONE, MOVEPOS, MOVETAN, ROTATETAN};

#define NUMBER_THREADS 4
GLThread* glThreads[NUMBER_THREADS];
int curThread = 0;
int startThread = 0;

//params for each of the threads EXCEPT start thread
//these are set in InitThread
double twist_params[NUMBER_THREADS];
double grav_params[NUMBER_THREADS];

#ifdef ISOTROPIC
double bend_params[NUMBER_THREADS];
#else
Matrix2d bend_params[NUMBER_THREADS];
#endif



Trajectory_Reader traj_reader(TRAJ_BASE_NAME);
vector<Thread> all_threads;
int thread_ind = 0;
int image_ind = 1;


float lastx_L=0;
float lasty_L=0;
float lastx_R=0;
float lasty_R=0;

float rotate_frame[2];
float move_end[2];
float tangent_end[2];
float tangent_rotation_end[2];


// double radii[NUM_PTS];
int pressed_mouse_button;

key_code key_pressed;



/* set up a light */
GLfloat lightOnePosition[] = {140.0, 0.0, 200.0, 0.0};
GLfloat lightOneColor[] = {0.99, 0.99, 0.99, 1.0};

GLfloat lightTwoPosition[] = {-140.0, 0.0, 200.0, 0.0};
GLfloat lightTwoColor[] = {0.99, 0.99, 0.99, 1.0};

GLfloat lightThreePosition[] = {140.0, 0.0, -200.0, 0.0};
GLfloat lightThreeColor[] = {0.99, 0.99, 0.99, 1.0};

GLfloat lightFourPosition[] = {-140.0, 0.0, -200.0, 0.0};
GLfloat lightFourColor[] = {0.99, 0.99, 0.99, 1.0};

/*
void applyControl(Thread* start, const VectorXd& u, VectorXd* res) {
  int N = glThreads[startThread]->getThread()->num_pieces();
  res->setZero(3*N);

  Vector3d translation;
  translation << u(0), u(1), u(2);

  double dw = 1.0 - u(3)*u(3) - u(4)*u(4) - u(5)*u(5);
  if (dw < 0) {
    cout << "Huge differential quaternion: " << endl;
  }
  dw = (dw > 0) ? dw : 0.0;
  dw = sqrt(dw);
  Eigen::Quaterniond q(dw, u(3),u(4),u(5));
  Matrix3d rotation(q);

  // apply the control u to thread start, and return the new config in res
  Frame_Motion toMove(translation, rotation);

  Vector3d end_pos = start->end_pos();
  Matrix3d end_rot = start->end_rot();
  toMove.applyMotion(end_pos, end_rot);
  start->set_end_constraint(end_pos, end_rot);
  start->minimize_energy();

  start->toVector(res);
}
*/

void computeDifference(Thread* a, Thread* b, VectorXd* res) {
  VectorXd avec;
  a->toVector(&avec);
  VectorXd bvec;
  b->toVector(&bvec);

  (*res) = avec - bvec;
}


void selectThread(int inc) {
  curThread = (curThread + inc) % NUMBER_THREADS;
  glutPostRedisplay();
}

void processLeft(int x, int y)
{
  if (key_pressed == MOVEPOS)
  {
    move_end[0] += (x-lastx_L)*MOVE_POS_CONST;
    move_end[1] += (lasty_L-y)*MOVE_POS_CONST;
  } else if (key_pressed == MOVETAN)
  {
    tangent_end[0] += (x-lastx_L)*MOVE_TAN_CONST;
    tangent_end[1] += (lasty_L-y)*MOVE_TAN_CONST;
  } else if (key_pressed == ROTATETAN)
  {
    tangent_rotation_end[0] += (x-lastx_L)*ROTATE_TAN_CONST;
    tangent_rotation_end[1] += (lasty_L-y)*ROTATE_TAN_CONST;
  }
  else {
    rotate_frame[0] += x-lastx_L;
    rotate_frame[1] += lasty_L-y;
  }

  lastx_L = x;
  lasty_L = y;
}

void processRight(int x, int y)
{
  //rotate_frame[0] += x-lastx_R;
  //rotate_frame[1] += y-lasty_R;

  if (key_pressed == MOVEPOS)
  {
    move_end[0] += (x-lastx_R)*MOVE_POS_CONST;
    move_end[1] += (lasty_R-y)*MOVE_POS_CONST;
  } else if (key_pressed == MOVETAN)
  {
    tangent_end[0] += (x-lastx_R)*MOVE_TAN_CONST;
    tangent_end[1] += (lasty_R-y)*MOVE_TAN_CONST;
  } else if (key_pressed == ROTATETAN)
  {
    tangent_rotation_end[0] += (x-lastx_R)*ROTATE_TAN_CONST;
    tangent_rotation_end[1] += (lasty_R-y)*ROTATE_TAN_CONST;
  }

  lastx_R = x;
  lasty_R = y;
}

void MouseMotion (int x, int y)
{
  if (pressed_mouse_button == GLUT_LEFT_BUTTON) {
    processLeft(x, y);
  } else if (pressed_mouse_button == GLUT_RIGHT_BUTTON) {
    processRight(x,y);
  }
  glutPostRedisplay ();
}

void processMouse(int button, int state, int x, int y)
{
  if (state == GLUT_DOWN)
  {
    pressed_mouse_button = button;
    if (button == GLUT_LEFT_BUTTON)
    {
      lastx_L = x;
      lasty_L = y;
    }
    if (button == GLUT_RIGHT_BUTTON)
    {
      lastx_R = x;
      lasty_R = y;
    }
    glutPostRedisplay ();
  }
}


void processSpecialKeys(int key, int x, int y) {
 /*if (key == GLUT_KEY_LEFT) {
   if(initialized) {
     if (curNode->prev != NULL) {
       curNode = curNode->prev;
       glThreads[7]->setThread(new Thread(curNode->x, VectorXd::Zero(curNode->N/3), Matrix3d::Identity()));
       glThreads[7]->minimize_energy();
       glutPostRedisplay();
     }
   }
 } else if (key == GLUT_KEY_RIGHT) {
   if(initialized) {
     if (curNode->next != NULL) {
       curNode = curNode->next;
       glThreads[7]->setThread(new Thread(curNode->x, VectorXd::Zero(curNode->N/3), Matrix3d::Identity()));
       glThreads[7]->minimize_energy();
       glutPostRedisplay();
     }
   }
 }
 */
}

void processNormalKeys(unsigned char key, int x, int y)
{
  if (key == 't') {
    key_pressed = MOVETAN;
  }
  else if (key == 'm') {
    key_pressed = MOVEPOS;
  }
  else if (key == 'r') {
    key_pressed = ROTATETAN;
  }
  else if (key == 'n') {
    thread_ind++;
    std::cout << "displaying thread " << thread_ind  << std::endl;
    if (thread_ind >= 0 && thread_ind < all_threads.size())
    {
			update_all_threads();
      glutPostRedisplay();
    }
  } else if (key == 'b') {
    thread_ind--;
    std::cout << "displaying thread " << thread_ind  << std::endl;
    if (thread_ind >= 0 && thread_ind < all_threads.size())
    {
			update_all_threads();
      glutPostRedisplay();
    }
  } else if (key == 'o') {
		//std::cout << std::endl;
		for (int i=1; i < NUMBER_THREADS; i++)
		{
			glThreads[i]->setThreadCoeffs();
#ifdef ISOTROPIC
			glThreads[i]->getThread()->minimize_energy(100000, 1e-10, 1.0, 1e-10);
#else
			glThreads[i]->getThread()->minimize_energy();
#endif
			//glThreads[i]->printThreadData();
		}
    glutPostRedisplay();
  } else if (key == 's') {
		save_opengl_image();
	} else if (key == 27) {
    exit(0);
  }

  lastx_R = x;
  lasty_R = y;

}

void processKeyUp(unsigned char key, int x, int y)
{
  if (key == '+') {
    selectThread(1);
  } else if (key == '-') {
    selectThread(-1);
  }
  key_pressed = NONE;
  move_end[0] = move_end[1] = tangent_end[0] = tangent_end[1] = tangent_rotation_end[0] = tangent_rotation_end[1] = 0.0;
}



void JoinStyle (int msg)
{
  exit (0);
}


int main (int argc, char * argv[])
{

  srand(time(NULL));
  srand((unsigned int)time((time_t *)NULL));

  printf("Instructions:\n"
      "Hold down the left mouse button to rotate image: \n"
      "\n"
      "Hold 'm' while holding down the right mouse to move the end\n"
      "Hold 't' while holding down the right mouse to rotate the tangent \n"
      "\n"
      "Press 'Esc' to quit\n"
      );

  InitGLUT(argc, argv);
  InitLights();
  InitStuff ();



  InitThread(argc, argv);

  // for (int i=0; i < NUM_PTS; i++)
  // {
  //   radii[i]=THREAD_RADII;
  // }

  glutMainLoop ();
}


GLuint sphereList;
void InitStuff (void)
{
  glClearColor(1.0f, 1.0f, 1.0f, 0.0f);
  //glClearColor(.05f, 0.05f, 0.05f, 0.0f);
  glEnable(GL_BLEND);
  glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
  //gleSetJoinStyle (TUBE_NORM_PATH_EDGE | TUBE_JN_ANGLE );
  rotate_frame[0] = 30.0;
  rotate_frame[1] = -75.0;

  sphereList = glGenLists(1);
  glNewList(sphereList, GL_COMPILE);
  glutSolidSphere(0.5,16,16);
  glEndList();
}

/* draw the helix shape */
void DrawStuff (void)
{
  glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glColor3f (0.8, 0.3, 0.6);

  glPushMatrix ();

  /* set up some matrices so that the object spins with the mouse */
  glTranslatef (0.0,0.0,-110.0);
  glRotatef (rotate_frame[1], 1.0, 0.0, 0.0);
  glRotatef (rotate_frame[0], 0.0, 0.0, 1.0);

  //change thread, if necessary
  if (move_end[0] != 0.0 || move_end[1] != 0.0 || tangent_end[0] != 0.0 || tangent_end[1] != 0.0 || tangent_rotation_end[0] != 0 || tangent_rotation_end[1] != 0)
  {
    glThreads[startThread]->ApplyUserInput(move_end, tangent_end, tangent_rotation_end);
	for (int i=0; i < NUMBER_THREADS; i++)
	{
		glThreads[i]->setThread((new Thread(*glThreads[startThread]->getThread())));
	}

  }


  //Draw Axes
  DrawAxes();

  glThreads[startThread]->updateThreadPoints();
  Vector3d display_start_pos = glThreads[startThread]->getStartPosition();


  for(int i = 0; i < NUMBER_THREADS; i++) {
    //Draw Thread
		//colors are R, G, B, Opacity
		if (i==0)
			continue;
    if (i==startThread) {
      glColor4f (0.8, 0.5, 0.0, 0.8);
    } else if (i==1) {
      //glColor4f (0.7, 0.3, 0.0, 0.8);
        glColor4f (190.0/255.0, 21.0/255.0, 22.0/255.0, 0.8);
    } else if (i==2) {
      glColor4f (17.0/255.0, 221.0/255.0, 50.0/255.0, 0.8);
    } else if (i==3) {
      glColor4f (13.0/255.0, 93.0/255.0, 225.0/255.0, 0.8);
    } else {
			//this shouldn't happen for now
      glColor4f (0.5, 0.5, 0.5, 1.0);
		}
    glThreads[i]->display_start_pos = display_start_pos;
    glThreads[i]->DrawThread();
    glThreads[i]->DrawAxes();
  }

  glPopMatrix ();
  glutSwapBuffers ();
}



void InitThread(int argc, char* argv[])
{

twist_params[1] = 10;
grav_params[1] = 1e-4;
#ifdef ISOTROPIC
bend_params[1] = 10;
#else
bend_params[1] << 1.0, 0.0, 0.0, 1.0;
#endif

twist_params[2] = 10.0;
grav_params[2] = 1e-4;
#ifdef ISOTROPIC
bend_params[2] = 1;
#else
bend_params[2] << 1.0, 0.0, 0.0, 10.0;
#endif



twist_params[3] = 1.0;
grav_params[3] = 1e-4;
#ifdef ISOTROPIC
bend_params[3] = 10;
#else
bend_params[3] << 10.0, 0.0, 0.0, 1.0;
#endif








  traj_reader.read_threads_from_file();
  all_threads = traj_reader.get_all_threads();

  for (int i=0; i < NUMBER_THREADS; i++)
  {
    glThreads[i] = new GLThread();
    glThreads[i]->setThread(new Thread(all_threads[thread_ind]));
    glThreads[i]->updateThreadPoints();



  }

	for (int i=1; i < NUMBER_THREADS; i++)
	{
		glThreads[i]->to_set_twist = twist_params[i];
		glThreads[i]->to_set_grav = grav_params[i];
#ifdef ISOTROPIC
		glThreads[i]->to_set_bend = bend_params[i];
#else
		glThreads[i]->to_set_B = bend_params[i];
#endif
	}


}


void DrawAxes()
{
  //Draw Axes
  glBegin(GL_LINES);
  glEnable(GL_LINE_SMOOTH);
  glColor3d(1.0, 0.0, 0.0); //red
  glVertex3f(0.0f, 0.0f, 0.0f); //x
  glVertex3f(10.0f, 0.0f, 0.0f);
  glColor3d(0.0, 1.0, 0.0); //green
  glVertex3f(0.0f, 0.0f, 0.0f); //y
  glVertex3f(0.0f, 10.0f, 0.0f);
  glColor3d(0.0, 0.0, 1.0); //blue
  glVertex3f(0.0f, 0.0f, 0.0f); //z
  glVertex3f(0.0f, 0.0f, 10.0f);

  //label axes
  void * font = GLUT_BITMAP_HELVETICA_18;
  glColor3d(1.0, 0.0, 0.0); //red
  glRasterPos3i(20.0, 0.0, -1.0);
  glutBitmapCharacter(font, 'X');
  glColor3d(0.0, 1.0, 0.0); //red
  glRasterPos3i(0.0, 20.0, -1.0);
  glutBitmapCharacter(font, 'Y');
  glColor3d(0.0, 0.0, 1.0); //red
  glRasterPos3i(-1.0, 0.0, 20.0);
  glutBitmapCharacter(font, 'Z');
  glEnd();
}


void InitGLUT(int argc, char * argv[]) {
  /* initialize glut */
  glutInit (&argc, argv); //can i do that?
  glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
  glutInitWindowSize(PIX_WIDTH,PIX_HEIGHT);
  glutCreateWindow ("Thread");
  glutDisplayFunc (DrawStuff);
  glutMotionFunc (MouseMotion);
  glutMouseFunc (processMouse);
  glutKeyboardFunc(processNormalKeys);
  glutSpecialFunc(processSpecialKeys);
  glutKeyboardUpFunc(processKeyUp);

  /* create popup menu */
  glutCreateMenu (JoinStyle);
  glutAddMenuEntry ("Exit", 99);
  glutAttachMenu (GLUT_MIDDLE_BUTTON);

  /* initialize GL */
  glClearDepth (1.0);
  glEnable (GL_DEPTH_TEST);
  glClearColor (0.0, 0.0, 0.0, 0.0);
  glShadeModel (GL_SMOOTH);

  glMatrixMode (GL_PROJECTION);
  /* roughly, measured in centimeters */
  glFrustum (-30.0, 30.0, -30.0, 30.0, 50.0, 500.0);
  glMatrixMode(GL_MODELVIEW);

   glEnable (GL_LINE_SMOOTH);
	 glEnable (GL_POLYGON_SMOOTH);
	 glHint (GL_POLYGON_SMOOTH, GL_NICEST);
   glEnable (GL_BLEND);
   glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
   glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE);
	glLineWidth (1.5);

}


void InitLights() {
  /* initialize lighting */
  glLightfv (GL_LIGHT0, GL_POSITION, lightOnePosition);
  glLightfv (GL_LIGHT0, GL_DIFFUSE, lightOneColor);
  glEnable (GL_LIGHT0);
  glLightfv (GL_LIGHT1, GL_POSITION, lightTwoPosition);
  glLightfv (GL_LIGHT1, GL_DIFFUSE, lightTwoColor);
  glEnable (GL_LIGHT1);
  glLightfv (GL_LIGHT2, GL_POSITION, lightThreePosition);
  glLightfv (GL_LIGHT2, GL_DIFFUSE, lightThreeColor);
  glEnable (GL_LIGHT2);
  glLightfv (GL_LIGHT3, GL_POSITION, lightFourPosition);
  glLightfv (GL_LIGHT3, GL_DIFFUSE, lightFourColor);
  glEnable (GL_LIGHT3);
  glEnable (GL_LIGHTING);
  glColorMaterial (GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);
  glEnable (GL_COLOR_MATERIAL);
}




void save_opengl_image()
{
  //playback and save images
  Mat img(PIX_HEIGHT, PIX_WIDTH, CV_8UC3);
  vector<Mat> img_planes;
  split(img, img_planes);

  uchar tmp_data[3][PIX_WIDTH*PIX_HEIGHT];

  GLenum read_formats[3];
  read_formats[0] = GL_BLUE;
  read_formats[1] = GL_GREEN;
  read_formats[2] = GL_RED;

  for (int i=0; i < 3; i++)
  {
    glReadPixels(0, 0, PIX_WIDTH, PIX_HEIGHT, read_formats[i], GL_UNSIGNED_BYTE, tmp_data[i]);
    img_planes[i].data = tmp_data[i];
  }


  merge(img_planes, img);
  flip(img, img, 0);

  char im_name[256];
  sprintf(im_name, "%s%d.png", IMG_SAVE_OPENGL, image_ind+1);
	image_ind++;
  imwrite(im_name, img);
  waitKey(1);
  //sleep(0);


}




void update_all_threads()
{
	for (int i=0; i < NUMBER_THREADS; i++)
	{
		glThreads[i]->setThread((new Thread(all_threads[thread_ind])));
	}

}
