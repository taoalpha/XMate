using Vsync;
using System;

namespace DataDefinition{

	[AutoMarshalled]
	public class profile{
		// Public fields will be included in the outform representation, fields with internal
		// keyword will not be included.
		public int FacebookID;
		public int ID;
		public string username;
		public int age;
		public string gender;

		public string preferredGender;
		//public int preferredAgeMin;
		//public int preferredAgeMax;
		public string city;
		public float latitude;
		public float longitude;
		public int credits;
		//public int rate;
		public float lastLoginTime;
		public float height;
		public float weight;

		public int[] scheduleList;
		//public int[] conflictlist;
		//public int[] historyPartner;
		//public int[] historyEvents;
		//public int[] unprocessedMessage;

		public int scheduleIndex;
		//public int conflictIndex;
		//public int histPartIndex;
		//public int histEventIndex;
		//public int messageIndex;

		// Null constructor: Needed for AutoMarshaller	
		public profile(){
			Console.WriteLine("Public initialization in profile");
		}

		// Internal construcotr used by the application to initialize a new object
		// Seems never invoked
		internal profile(int id, int fbID, string name, int old, string sex, 
			string preferSex, string cityLoc, float lat, float longi, int credit, 
			float time, float tall, float pound){
			ID = id;
			FacebookID = fbID;
			username = name;
			age = old;
			gender = sex;
			preferredGender = preferSex;
			city = cityLoc;
			latitude = lat;
			longitude = longi;
			credits = credit;
			lastLoginTime = time;
			height = tall;
			weight = pound;
			//scheduleIndex = 0;
			//scheduleList = new int[16];
			Console.WriteLine("Internal initialization");
		}

		//public byte[] toBArray(){
		//	Console.WriteLine("profile to array");
		//	return Vsync.Msg.toBArray(FacebookID, ID,username);
		//}

		//public profile(byte[] ba){
		//	object[] obs = Msg.BArrayToObjects(ba); 
		//	int idx = 0;
		//	FacebookID = (int)obs[idx++];
		//	ID = (int)obs[idx++];
		//	username = (string) obs[idx++];
		//	Console.WriteLine("byte array to profile");
		//}

		public void addScheduleToList(int scheduleID){
			if (scheduleList == null){
				scheduleList = new int[16];
			}else if (scheduleIndex + 1 == scheduleList.Length){
				int[] temp = new int[scheduleList.Length * 2];
				for (int i = 0; i < scheduleList.Length; i++){
					temp[i] = scheduleList[i];
				}
				scheduleIndex = scheduleList.Length;
				scheduleList = temp;
			}
			scheduleList[scheduleIndex] = scheduleID;
			Console.WriteLine("Add a schedule to user's schedule list");
		}

		public override string ToString(){
			string res =  "Get profile for user ID " + ID + " " + username + " with schedule ";
			if (scheduleList != null){
				for (int i = 0; i < scheduleList.Length; i++){
					if (scheduleList[i] == 0){
						break;
					}
					res += scheduleList[i] + " ";
				}
			}
			return res;
		}
	}

	//[AutoMarshalled]
	//public class post{
		//fields

	// Null constructor: Needed for AutoMarshaller
	//	public post(){}

	// Internal construcotr used by the application to initialize a new object
	//	internal post(int id){}
	//}

	//[AutoMarshalled]
	//public class historyPost{
		//fields

	// Null constructor: Needed for AutoMarshaller
	//	public historyPost(){}

	// Internal construcotr used by the application to initialize a new object
	//	internal historyPost(int id){}
	//}

	//[AutoMarshalled]
	//public class message{
		//fields

	// Null constructor: Needed for AutoMarshaller
	//	public message(){}

	// Internal construcotr used by the application to initialize a new object
	//	internal message(int id){}
	//}

	public class register{
		const byte profileTID = 0;
		//const byte postTID = 1;
		//const byte historyPostTID = 2;
		//const byte mssageTID = 3;
 

		public register(){
			initialize();
		}

		public void initialize(){
			Vsync.Msg.RegisterType(typeof(profile), profileTID);
		//	Vsync.Msg.RegisterType(typeof(post), postTID);
		//	Vsync.Msg.RegisterType(typeof(historyPost), historyPostTID);
		//	Vsync.Msg.RegisterType(typeof(message), mssageTID);
			Console.WriteLine("Registered self-defined data types");						
		}	
	}
}