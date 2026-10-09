from pathlib import Path
import json,re
H=Path(__file__).resolve().parent
ROOT=H.parents[1]
S=ROOT/'Final Presentation/Speaking/simple_speech'
data=json.loads((S/'script.json').read_text(encoding='utf-8'))

def revise(n,opening,*paragraphs,after=None):
    s=data[n-1];s['opening']=opening;s['paragraphs']=list(paragraphs)
    if after is not None:s['after_video']=after

revise(1,'Hello everyone, and thank you for being here.',
 'Today, I will present my work on controlling a seven-joint robot for grinding. The goal is to help the tool align with a surface while reducing unwanted motion of the arm.')
revise(2,'First, let me explain why tool alignment matters.',
 'For grinding, the tool face needs to align with the surface. However, the real surface angle may differ from the angle used by the controller. Moreover, joint friction can also affect the tool orientation. The controller therefore allows the tool to rotate passively during contact, helping it align with the real surface. This video shows the idea.',
 after='As you can see, the tool rotates even though its desired orientation remains fixed.')
revise(3,'With that goal in mind, here is the structure of the presentation.',
 'I will first explain the controller, then show the contact experiments and their results. After that, I will discuss the extra joint motion and the null-space controller, before summarizing the main findings.')
revise(4,'To explain the controller, I will start with the tool pose.',
 'The pose describes where the tool is and how it is rotated. It has three position coordinates and three orientation coordinates. Using forward kinematics, we calculate this pose from the seven measured joint angles.')
revise(5,'We can now describe the directions in which the tool interacts with the surface.',
 'The normal points out of the surface, while the two tangents lie along it. These directions define the force and moment components, allowing us to choose where the tool should be compliant and where it should remain stiff.')
revise(6,'Cartesian impedance control gives this interaction the behaviour of a spring and a damper.',
 'Reading the force equation, f equals K p times e p, plus D p times the velocity error. Here, e p is the desired position minus the measured position. The stiffness term therefore pulls the tool towards its target. The damping term uses desired minus measured velocity, so for a fixed target it opposes motion.',
 'The moment equation follows the same pattern: m equals K R times e R, plus D R times the angular-velocity error. Here, e R is the rotation angle times its axis. Force and moment form the wrench F below. The zero off-diagonal blocks keep translation and rotation separate at the compliance reference. Lower stiffness allows more displacement under a given load, while damping reduces oscillation.')
revise(7,'To apply this wrench, the controller must convert it into joint torques.',
 'The first equation, tau equals J transpose F, maps the force and moment to all seven joints. In the feedback direction, x dot equals J times q dot gives the tool velocity from joint velocities. We then add the null-space torque and Coriolis compensation to the Cartesian torque. However, gravity compensation is handled internally by the robot. This loop repeats every millisecond.')
revise(8,'We can also choose where the virtual spring and damper act.',
 'The tool centre point, or TCP, is our controlled point on the end effector, or EE. The centre of compliance, or CoC, is the virtual reference for stiffness and damping. Shifting this reference introduces a lever effect. The equation m at the TCP equals r c cross f describes the added moment: it depends on both the displacement and force directions.')
revise(9,'Whether that moment helps depends on the direction of the shift.',
 'On the left, the added moment supports alignment; on the right, it opposes alignment. The CoC shift must therefore be chosen to match the initial angular offset of the tool.')
revise(10,'The equations here show how we introduce that coupling into the controller.',
 'The displacement r c runs from the TCP to the CoC. It defines the point-shift adjoint matrix A, written as Ad of r c. We use it to transform both matrices: K at the TCP equals A transpose K c A, and D at the TCP equals A transpose D c A. The right-hand A maps errors and velocities to the CoC; A transpose maps the resulting wrench back to the TCP.',
 'These transformed matrices generally have nonzero off-diagonal blocks. A position error can therefore create a moment, and an orientation error can create a force. The damping blocks similarly couple linear and angular velocity errors. This is how the CoC shift changes the force and turning response together.')
revise(11,'With the controller defined, I can now show the contact experiment.',
 'I deliberately start with an angular offset to represent a mismatch between the assumed and real surface orientations. The robot then approaches, makes contact and performs the grinding motion. Motion along the normal and rotation about the two tangent axes are compliant, while the other directions remain stiff.')
revise(12,'Before assessing alignment, I first checked the basic impedance response.',
 'For this test, I pushed and rotated the tool by hand, as shown in the video.',
 after='The next two plots compare the commanded and estimated values with the spring-law predictions. It is important to note that the estimated values are model-based measurements.')
revise(13,'Let us first check the force against the spring term K p times e p.',
 'A displacement of about twenty millimetres predicts approximately minus twenty newtons. The commanded mean is almost the same, while the model estimate is slightly larger. Both means below the plot use the shaded steady-state interval.')
revise(14,'The rotational test checks the corresponding term K R times e R.',
 'A rotation of about six and a half degrees gives predicted and commanded mean moments of roughly one point seven newton metres. The estimated mean is slightly higher. Again, the means use the shaded interval. Together, these tests support the expected spring behaviour.')
revise(15,'We can now look at the wrench during actual contact alignment.',
 'In this separate test, the force curves remain close. However, the model-estimated moment is larger during alignment because it includes the contact moment from the surface, which helps turn the tool. Once the motion settles, the values become close again.')
revise(16,'To understand this turning response, I first varied the rotational stiffness.',
 'The plot shows the remaining angular error relative to the calibrated surface; closer to zero means better alignment in this direction. Higher rotational stiffness leaves a larger error because it resists the rotation caused by contact.')
revise(17,'Next, I varied the centre of compliance to change the coupling.',
 'For a positive starting offset, a positive CoC shift helps alignment, whereas a negative starting offset benefits from a different CoC position. A larger shift is therefore not always better: its direction and size must match the initial angular offset.')
revise(18,'The time histories show how this difference develops.',
 'A supporting CoC shift helps alignment happen faster, while an opposing shift leaves much of the initial angular error. The normal forces are broadly similar, but the moments differ. In these tests, the CoC shift therefore mainly changes the rotational response.')
revise(19,'So far, we have controlled the tool; the null-space controller manages the extra motion of the arm.',
 'With seven joints and six independent tool-pose coordinates, seven minus six leaves one extra degree of freedom. The condition J times q dot null equals zero means that these joint velocities produce no instantaneous tool motion. The arm can therefore change posture while the main controller holds the tool pose.',
 'The secondary torques are projected to preserve the main tool-pose task in the controller model. Damping opposes the extra joint velocity and becomes zero at rest. Conditioning instead depends on the joint configuration and can act even at rest. It moves the posture towards a larger minimum singular value of J, called sigma min, helping avoid directions in which tool motion becomes difficult. The two torques thus address motion and posture, respectively.')
revise(20,'The first video shows the effect of damping.',
 'It starts with null-space control off, then switches the damping torque on.',
 after='With null-space control off, the arm moves more easily. With damping on, the same push moves it more slowly, so I need to push harder to reach the same speed. Throughout this, the main controller still holds the tool pose.')
revise(21,'Conditioning has a different purpose, as this next video shows.',
 'Here, the conditioning controller is active.',
 after='It changes the posture while keeping the tool pose. Unlike damping, which mainly opposes motion, conditioning seeks a posture with better Jacobian conditioning.')
revise(22,'To compare these effects systematically, I applied the same disturbance in each experiment.',
 'Joint torques represent a virtual twenty-newton force acting on joint three. I tested no null-space control, damping only, conditioning only, and both together, with three trials per case. Joint one receives the largest peak disturbance torque, so the next plots show its mean response over four seconds.')
revise(23,'First, we compare how much joint one moves.',
 'Damping reduces the motion, while conditioning and the combined controller keep it much smaller. The zoom on the right reveals repeated direction changes. Adding damping reduces the total motion, although some reversals remain.')
revise(24,'We also need to check whether the resulting posture remains well conditioned.',
 'Without null-space control, sigma min decreases, and damping alone gives the same trend. With conditioning, alone or combined with damping, it stays almost constant. This supports the distinction made earlier: damping limits motion, while conditioning helps maintain a usable posture.')
revise(25,'These results bring me to the main conclusions.',
 'Allowing the tool to rotate during contact helps reduce the angular error. The CoC shift can support or oppose this alignment, while higher rotational stiffness resists it and leaves a larger error. For the arm, damping reduces unwanted motion and conditioning improves the posture response; the two can be combined.',
 'As future work, I would improve the tool mount and adjust the CoC during alignment, returning it to the TCP afterwards. Thank you for your attention. I am happy to take your questions.')
revise(26,'This extra video illustrates why the direction of the CoC shift matters.',
 'Here, the added moment acts against alignment.',
 after='It is the opposing case from the earlier diagrams: the shift hinders the turning motion. The result plots provide the numerical comparison.')
revise(27,'This slide gives the detailed equations for the two null-space torques.',
 'The torque projector selects secondary directions that preserve the main tool-pose task in the controller model. The damping term opposes projected joint velocity, so it vanishes when the joints stop. The conditioning term instead selects the direction with a better sigma min and can act at rest. Its small deadband prevents unnecessary switching between directions.')
revise(28,'This diagram distinguishes the two angular quantities used in the results.',
 'The red arc is the angular offset at contact entry, while the blue arc is the remaining angular error. Both are measured relative to the calibrated surface. The plots show the component about the first surface tangent, so zero in that component alone does not guarantee perfect physical alignment.')
revise(29,'This baseline keeps the CoC at the TCP.',
 'Contact reduces the two large starting offsets, but the three final errors remain around one and a half degrees. Friction, calibration and the tool mount may contribute to the remaining error; this comparison does not separate their effects.')
revise(30,'The mismatch at contact entry can come from two sources.',
 'The real surface may differ from the surface assumed by the controller, and the actual tool orientation may differ from its desired orientation. The green tool face and dashed desired orientation illustrate the latter. Both affect the entry angle, which is why the contact tests use a deliberate angular offset.')
revise(31,'Finally, this comparison adds up motion across all seven joints.',
 'Because motion is accumulated over time, changes of direction do not cancel. Damping alone gives about twenty-five percent less motion than no null-space torque. At a conditioning setting of two newton metres, adding damping gives about fifty percent less motion than conditioning alone.')

(H/'script.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
count=lambda ds:sum(len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*",' '.join([s['opening'],*s['paragraphs'],s.get('after_video','')]))) for s in ds)
w=count(data[:25]);v=sum(s.get('video_seconds',0) for s in data[:25])
print(json.dumps({'main_words':w,'backup_words':count(data[25:]),'minutes_at_130':w/130+(v+30)/60,'wpm_for_15':w/(15-(v+30)/60)},indent=2))
