using Vsync;

namespace DataDefinition{

	[AutoMarshalled]
	public class userProfile{
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
		// TODO history partner history [User Id]
		// TODO history events [Post Id]]
		// TODO Unprocessed Message[ {Type:(Read but not processed/Unread),Message Id}, ]

		// Null constructor: Needed for AutoMarshaller	
		public userProfile(){
		}

		internal userProfile(int fbID, int ID, string name){
			FacebookID = fbID;
			id = ID;
			username = name;
		}

	}

	//internal const byte TID = 123; 
	//Vsync.Msg.RegisterType(typeof(userProfile), 123);
}