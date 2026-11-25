using System;
using System.Security.Cryptography;
using System.Text;

class Program
{
    static void Main()
    {
        string plainText = "Hello it s Aymen";

        using (Aes aes = Aes.Create())
        {
            aes.Mode = CipherMode.CFB;
            aes.Padding = PaddingMode.PKCS7;

            aes.Key = new byte[32]
            {
                0x9f, 0xbd, 0xe6, 0x4f, 0xad, 0xe1, 0xf3, 0x9d,
                0x5e, 0x53, 0x7f, 0xbb, 0x92, 0x96, 0x85, 0x10,
                0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10
            };
            aes.IV = new byte[16]
            {
                0xd7, 0xc9, 0xc5, 0xaf, 0x7f, 0xd1, 0xe8, 0x9e,
                0x83, 0xbe, 0x8c, 0xa9, 0xac, 0x7e, 0xd0, 0x00
            };

            byte[] plainBytes = Encoding.UTF8.GetBytes(plainText);

            byte[] encryptedBytes;
            using (ICryptoTransform encryptor = aes.CreateEncryptor(aes.Key, aes.IV))
            {
                encryptedBytes = encryptor.TransformFinalBlock(plainBytes, 0, plainBytes.Length);
            }

            byte[] decryptedBytes;
            using (ICryptoTransform decryptor = aes.CreateDecryptor(aes.Key, aes.IV))
            {
                decryptedBytes = decryptor.TransformFinalBlock(encryptedBytes, 0, encryptedBytes.Length);
            }

            string decryptedText = Encoding.UTF8.GetString(decryptedBytes);

            Console.WriteLine("Mode: " + aes.Mode);
            Console.WriteLine("Encrypted (Base64): " + Convert.ToBase64String(encryptedBytes));
            Console.WriteLine("Decrypted: " + decryptedText);
            Console.WriteLine("Match: " + (plainText == decryptedText));
        }
    }
}
