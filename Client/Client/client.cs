using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.IO;

namespace Client
{
    class client
    {

        static void Main(string[] args)
        {
            // File reading code from https://support.microsoft.com/en-gb/help/816149/how-to-read-from-and-write-to-a-text-file-by-using-visual-c
            String line;
            List<String> lines = new List<String>();
            try
            {
                //Pass the file path and file name to the StreamReader constructor
                StreamReader sr = new StreamReader("../../../../../CementCrow/DataFile.txt");

                //Read the first line of text
                line = sr.ReadLine();

                //Continue to read until you reach end of file
                while (line != null)
                {
                    //Read the next line
                    line = sr.ReadLine();
                    lines.Add(line);
                }

                //close the file
                sr.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("Exception: " + e.Message);
            }
            finally
            {
                Console.WriteLine("Executing finally block.");
            }


            Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            IPEndPoint ipLocal = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8221);

            bool connected = false;

            while (connected == false)
            {
                try
                {
                    s.Connect(ipLocal);
                    connected = true;
                }
                catch (Exception)
                {
                    Thread.Sleep(1000);
                }
            }

            int ID = 0;


            ASCIIEncoding encoder = new ASCIIEncoding();
            byte[] buffer = new byte[4096];

            while (true)
            {
                //Loop through all lines
                for (int i = 0; i < lines.Count - 1; i++)
                {
                    String Msg = (lines[i] + "!");

                    Console.WriteLine(Msg);
                    ID++;

                    buffer = encoder.GetBytes(Msg);

                    try
                    {
                        int bytesSent = s.Send(buffer);
                    }
                    catch (System.Exception ex)
                    {
                        Console.WriteLine(ex);
                    }
                    
                }
                Console.ReadLine();
            }
        }
    }
}
