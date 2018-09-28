from solver import rk4Quaternion
import numpy as np
import frames
import unittest
import satellite
from dynamics import x_dot_BO
from constants_1U import G, M_EARTH, v_w_IO_o

def f_constant(sat):
	return 1.0

class TestSolver(unittest.TestCase):
	
	def test_constant(self):
		t0 = 0.0
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),t0)
		t = 10
		mySat.setPos(np.array([1e6,0.,0.]))
		mySat.setVel(np.array([5.0,5.0,0.0]))
		h = 0.1
		for i in range(0,int(t/h)):
			x1 = rk4Quaternion(mySat,f_constant,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)
		self.assertTrue(np.allclose([10.0,10.0,10.0],mySat.getW_BO_b()))
	
	def test_dynamics(self):
		t0 = 0.
		h = 0.001
		
		v_q_BO = np.array([0.4,0.254,-0.508,0.71931912])
		
		v_w_BO_b = frames.wBIb2wBOb(np.array([0.1,-0.05,-0.3]),v_q_BO,v_w_IO_o)
		
		mySat = satellite.Satellite(np.hstack((v_q_BO, v_w_BO_b)),t0)
		
		mySat.setPos(np.array([1e6,53e5,0.]))
		mySat.setVel(np.array([5.60,-5.0,0.0]))
		mySat.setDisturbance_b(np.array([10e-10,-4e-6,-3e-5]))
		mySat.setControl_b(np.array([1e-5,1e-5,-8e-4]))
		
		
		x1 = rk4Quaternion(mySat,x_dot_BO,h)
		mySat.setState(np.hstack((v_q_BO,v_w_BO_b)))		
		k1 = h*x_dot_BO(mySat)
		mySat.setState(np.hstack((v_q_BO,v_w_BO_b))+0.5*k1)
		k2 = h*x_dot_BO(mySat)
		mySat.setState(np.hstack((v_q_BO,v_w_BO_b))+0.5*(k2+k1))
		k3 = h*x_dot_BO(mySat)
		mySat.setState(np.hstack((v_q_BO,v_w_BO_b))+k3+0.5*(k2+k1))
		k4 = h*x_dot_BO(mySat)
		
		error_state = np.hstack((v_q_BO,v_w_BO_b)) + (1./6.)*(k1 + 2.*k2 + 2.*k3 + k4)
		print(error_state)
		self.assertTrue(np.allclose(error_state,x1))
	
if __name__=="__main__":
	unittest.main(verbosity=2)