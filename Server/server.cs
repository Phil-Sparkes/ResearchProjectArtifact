using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.Net;
using System.Net.Sockets;
using System.Threading;



#if TARGET_LINUX
using Mono.Data.Sqlite;
using sqliteConnection 	=Mono.Data.Sqlite.SqliteConnection;
using sqliteCommand 	=Mono.Data.Sqlite.SqliteCommand;
using sqliteDataReader	=Mono.Data.Sqlite.SqliteDataReader;
#endif

#if TARGET_WINDOWS
using System.Data.SQLite;
using sqliteConnection = System.Data.SQLite.SQLiteConnection;
using sqliteCommand = System.Data.SQLite.SQLiteCommand;
using sqliteDataReader = System.Data.SQLite.SQLiteDataReader;
#endif


namespace Server
{
    class server
    {
        static bool quit = false;

        public static string heatmapDatabase = "data.database";
        public static sqliteConnection conn = new sqliteConnection("Data Source=" + heatmapDatabase + ";Version=3;FailIfMissing=True");


        static LinkedList<String> incommingMessages = new LinkedList<string>();

        class ReceiveThreadLaunchInfo
        {
            public ReceiveThreadLaunchInfo(int ID, Socket socket)
            {
                this.ID = ID;
                this.socket = socket;
            }

            public int ID;
            public Socket socket;

        }

        static void acceptClientThread(Object obj)
        {
            Socket s = obj as Socket;

            int ID = 1;

            while (quit == false)
            {
                var newClientSocket = s.Accept();

                var myThread = new Thread(clientReceiveThread);
                myThread.Start(new ReceiveThreadLaunchInfo(ID, newClientSocket));

            }
        }

        static void clientReceiveThread(Object obj)
        {
            ReceiveThreadLaunchInfo receiveInfo = obj as ReceiveThreadLaunchInfo;
            bool socketLost = false;

            while ((quit == false) && (socketLost == false))
            {
                byte[] buffer = new byte[4094];

                try
                {
                    int result = receiveInfo.socket.Receive(buffer);

                    if (result > 0)
                    {
                        ASCIIEncoding encoder = new ASCIIEncoding();

                        lock (incommingMessages)
                        {
                            incommingMessages.AddLast(encoder.GetString(buffer, 0, result));
                        }
                    }
                }
                catch (System.Exception ex)
                {
                    socketLost = true;
                }
            }
        }
        static void Main(string[] args)
        {
            sqliteConnection.CreateFile(heatmapDatabase);
            conn.Open();

            sqliteCommand command;

            command = new sqliteCommand("create table if not exists table_hitLocation (X float, Y float)", conn);
            command.ExecuteNonQuery();

            ASCIIEncoding encoder = new ASCIIEncoding();

            Socket serverClient = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            IPEndPoint ipLocal = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8221);

            serverClient.Bind(ipLocal);
            serverClient.Listen(4);

            Console.WriteLine("Waiting for client ...");

            var myThread = new Thread(acceptClientThread);
            myThread.Start(serverClient);
            String messageToRead = "";

            byte[] buffer = new byte[4096];

            while (true)
            {
                lock (incommingMessages)
                {
                    if (incommingMessages.First != null)
                    {
                        messageToRead = incommingMessages.First.Value;

                        incommingMessages.RemoveFirst();

                    }
                }
                if (messageToRead != "")
                {
                    String[] substrings = messageToRead.Split('!');
                    for (int i = 0; i < substrings.Length - 1; i++)
                    {
                        // extract coordinates
                        String singleMessage = substrings[i];
                        String[] coordinateValues = singleMessage.Split(',');
                        float xValue = float.Parse(coordinateValues[0]);
                        float yValue = float.Parse(coordinateValues[1]);
                        messageToRead = "";
                        Console.WriteLine(xValue + ", " + yValue);

                        // insert to table
                        var sql = "insert into " + "table_hitLocation" + " (x, y) values ";
                        sql += "('" + xValue + "'";
                        sql += ",";
                        sql += "'" + yValue + "'";
                        sql += ")";
                        command = new sqliteCommand(sql, conn);
                        command.ExecuteNonQuery();
                    }
                }
                Thread.Sleep(1);
            }
        }
    }
}
