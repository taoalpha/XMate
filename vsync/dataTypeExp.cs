using Vsync;
using System;

namespace DataDefinition{

	[AutoMarshalled]
	public class profile{
		// Public fields will be included in the outform representation, fields with internal
		// keyword will not be included.
		public int FacebookID;
		public int id;
		public string username;
		//public int age;
		//public string preferredGender;
		//public string preferredAgeRange;
		//public string city;
		//public string latitude;
		//public string longitude;
		//public int rate;
		//public int credits;
		//public int lastLoginTime;
		//public float Height;
		//public float Weight;
		//public string gender;
		// TODO schedule list
		public scheduleUser[] scheduleList;
		internal int scheduleIndex;
		// TODO history partner history [User Id]
		// TODO history events [Post Id]]
		// TODO Unprocessed Message[ {Type:(Read but not processed/Unread),Message Id}, ]

		// Null constructor: Needed for AutoMarshaller	
		public profile(){
			scheduleIndex = 0;
			Console.WriteLine("Public intialization for user profile");
		}

		internal profile(int fbID, int ID, string name, scheduleUser[] schedules){
			FacebookID = fbID;
			id = ID;
			username = name;
			scheduleList = schedules;
			scheduleIndex = 0;
			Console.WriteLine("Internal intialization for user profile");
		}

		public byte[] toBArray(){
			Console.WriteLine("Convert from user profile to byte array");
			return Vsync.Msg.toBArray(FacebookID, id,username, scheduleList);
		}

		public profile(byte[] ba){
			object[] obs = Msg.BArrayToObjects(ba); 
			int idx = 0;
			FacebookID = (int)obs[idx++];
			id = (int)obs[idx++];
			username = (string) obs[idx++];
			scheduleList = new scheduleUser[obs.Length - idx];
			scheduleIndex = 0;
			while (id < obs.Length){
				scheduleList[scheduleIndex++] = (scheduleUser) obs[idx++];
			}
			Console.WriteLine("Convert from byte array to user profile");
		}

		public void addScheduleToList(scheduleUser sche){
			if (scheduleList == null){
				scheduleList = new scheduleUser[16];
			}else if (scheduleIndex + 1 == scheduleList.Length){
				scheduleUser[] temp = new scheduleUser[scheduleList.Length * 2];
				for (int i = 0; i < scheduleList.Length; i++){
					temp[i] = scheduleList[i];
				}
				scheduleIndex = scheduleList.Length;
				scheduleList = temp;
			} 
			scheduleList[scheduleIndex++] = sche;
			Console.WriteLine("Add schedule to user's schedule list");
		}

		public override string ToString(){
			string res = FacebookID + " " + id + " " + username;
			for (int i = 0; i < scheduleList.Length; i++){
				res += scheduleList[i].ToString() + " ";
			}
			return res;
		}
	}


	[AutoMarshalled]
	public class scheduleUser{
		public int postID;
		public bool conflict;

		public scheduleUser(){
			Console.WriteLine("Public intialization for scheduleUser");
		}

		internal scheduleUser(int scheduleID, bool conf){
			postID = scheduleID;
			conflict = conf;
			Console.WriteLine("Internal intialization in scheduleUser");
		}

		public byte[] toBArray(){
			Console.WriteLine("Convert from scheduleUser to byte array");
			return Vsync.Msg.toBArray(postID, conflict);
		}

		public scheduleUser(byte[] ba){
			object[] obs = Msg.BArrayToObjects(ba);
			int idx = 0;
			postID = (int) obs[idx++];
			conflict = (bool) obs[idx++];
			Console.WriteLine("Convert from byte array to scheduleUser");
		}

		public override string ToString(){
			return postID + " " + conflict;
		}
	}

	public class initializer{
		const byte profileTID = 123; 
		const byte scheduleUserTID = 124;

		public initializer(){
			initialize();
		}

		public void initialize(){
			Vsync.Msg.RegisterType(typeof(scheduleUser),scheduleUserTID);
			Vsync.Msg.RegisterType(typeof(profile), profileTID);
			Console.WriteLine("Registered profile and scheduleUser");			
		}	
	}
}