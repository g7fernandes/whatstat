#whatstat

This program counts the number of times each user sent a message to a WhatsApp group using the backup file. 
To get the backup file in the .txt format, go to a group and in the settings go on Export Chat. Then export without attachments,
doing so will be faster and it allows a bigger chat file. Whatsapp export a maximum number of messages of 40000.

Save the .txt file that whatsapp exported in the same folder where the program is located. After running python whatstat, the 
program will ask the name of the file (with extension).

This program works with whatsapp installed in a smartphone in English, Portuguese, German or French. The way which whastapp writes 
the date varies with language. 

The program rank the members by number of messages, build graph of message frequency of selected members, and calculates the 
correlation. To make an smoother graph, the frenquency ploted is calculated in a window of time that moves. A correlation is
also calculated that shows which members usually talk at the same time. 

The program comments and options is in Portuguese, but almost all words used are cognates with English and Spanish, anyone that
speaks this languages can understand enough to use.

Some Windows users complain codification errors after opening the file with Notepad. I recommend using Notepad++ or Kate to edit 
the file instead. 

The program requires matplotlib and numpy. You can install with PIP or use Anaconda Python distribution. 

