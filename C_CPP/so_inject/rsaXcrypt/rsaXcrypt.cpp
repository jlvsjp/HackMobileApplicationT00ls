//demo.cpp
// g++ demo.cpp -o demo -lcrypto
#include <openssl/rsa.h>
#include <openssl/err.h>
#include <openssl/pem.h>

#include <iostream>
#include <string>
#include <cstring>
#include <cassert>
#include <malloc.h>
#include <unistd.h>
using namespace std;

static const std::string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

std::string base64_encode(unsigned const char* , unsigned int len);
std::string base64_decode(std::string const& s);

static inline bool is_base64(unsigned char c) {
    return (isalnum(c) || (c == '+') || (c == '/'));
}

std::string base64_encode(unsigned const char* bytes_to_encode, unsigned int in_len) {
    std::string ret;
    int i = 0;
    int j = 0;
    unsigned char char_array_3[3];
    unsigned char char_array_4[4];

    while (in_len--) {
        char_array_3[i++] = *(bytes_to_encode++);
        if (i == 3) {
            char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
            char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
            char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
            char_array_4[3] = char_array_3[2] & 0x3f;

            for(i = 0; (i <4) ; i++)
                ret += base64_chars[char_array_4[i]];
            i = 0;
        }
    }

    if (i)
    {
        for(j = i; j < 3; j++)
            char_array_3[j] = '\0';

        char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
        char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
        char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
        char_array_4[3] = char_array_3[2] & 0x3f;

        for (j = 0; (j < i + 1); j++)
            ret += base64_chars[char_array_4[j]];

        while((i++ < 3))
            ret += '=';

    }

    return ret;

}

std::string base64_decode(std::string const& encoded_string) {
    int in_len = encoded_string.size();
    int i = 0;
    int j = 0;
    int in_ = 0;
    unsigned char char_array_4[4], char_array_3[3];
    std::string ret;

    while (in_len-- && ( encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
        char_array_4[i++] = encoded_string[in_]; in_++;
        if (i ==4) {
            for (i = 0; i <4; i++)
                char_array_4[i] = base64_chars.find(char_array_4[i]);

            char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
            char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
            char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

            for (i = 0; (i < 3); i++)
                ret += char_array_3[i];
            i = 0;
        }
    }

    if (i) {
        for (j = i; j <4; j++)
            char_array_4[j] = 0;

        for (j = 0; j <4; j++)
            char_array_4[j] = base64_chars.find(char_array_4[j]);

        char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
        char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
        char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

        for (j = 0; (j < i - 1); j++) ret += char_array_3[j];
    }

    return ret;
}

//加密
std::string EncodeRSAKeyFile(const std::string& strPemFileName, const std::string& strData, bool usePub)
{
    int ret = 0;
    if (strPemFileName.empty() || strData.empty()){
        assert(false);
        return "";
    }
    FILE* hKeyFile = fopen(strPemFileName.c_str(), "rb");
    if(hKeyFile == NULL){
        assert(false);
        return "";
    }
    std::string strRet;
    RSA* pRSAKey = RSA_new();

    //读秘钥文件
    if(usePub){
        if(PEM_read_RSA_PUBKEY(hKeyFile, &pRSAKey, 0, 0) == NULL){
            cout << "read RSAPublicKey Error!" << endl;
            assert(false);
            return "";
        }
    }else{
        if(PEM_read_RSAPrivateKey(hKeyFile, &pRSAKey, 0, 0) == NULL){
            cout << "read RSAPrivateKey Error!" << endl;
            assert(false);
            return "";
        }
    }

    int nLen = RSA_size(pRSAKey);
    char* pEncode = new char[nLen + 1];
    if(usePub){
        ret = RSA_public_encrypt(
            strData.length(),
            (const unsigned char*)strData.c_str(),
            (unsigned char*)pEncode,
            pRSAKey,
            RSA_PKCS1_PADDING
//            RSA_NO_PADDING
        );
    }else{
        ret = RSA_private_encrypt(
            strData.length(),
            (const unsigned char*)strData.c_str(),
            (unsigned char*)pEncode,
            pRSAKey,
            RSA_PKCS1_PADDING
//            RSA_NO_PADDING
        );
    }
    if (ret > 0){
        strRet = std::string(pEncode, ret);
    }else{
        cout << "encrypt failed!" << endl;
    }
    delete[] pEncode;
    RSA_free(pRSAKey);
    fclose(hKeyFile);
    CRYPTO_cleanup_all_ex_data();
    return strRet;
}

//解密
std::string DecodeRSAKeyFile(const std::string& strPemFileName, const std::string& strData, bool usePub)
{

    int ret = 0;
    if (strPemFileName.empty() || strData.empty()){
        assert(false);
        return "";
    }
    FILE* hKeyFile = fopen(strPemFileName.c_str(),"rb");
    if( hKeyFile == NULL ){
        assert(false);
        return "";
    }
    std::string strRet;
    RSA* pRsaKey = RSA_new();

    //读秘钥文件
    if(usePub){
        if(PEM_read_RSA_PUBKEY(hKeyFile, &pRsaKey, 0, 0) == NULL){
            cout << "read RSAPublicKey Error!" << endl;
            assert(false);
            return "";
        }
    }else{
        if(PEM_read_RSAPrivateKey(hKeyFile, &pRsaKey, 0, 0) == NULL){
            cout << "read RSAPrivateKey Error!" << endl;
            assert(false);
            return "";
        }
    }

    int nLen = RSA_size(pRsaKey);
    char* pDecode = new char[nLen+1];

    if(usePub){
        // cout << "Decrypting...(public key)" << endl;
        ret = RSA_public_decrypt(
            strData.length(),
            (const unsigned char*)strData.c_str(),
            (unsigned char*)pDecode,
            pRsaKey,
            RSA_PKCS1_PADDING
//            RSA_NO_PADDING
        );
    }

    else{
        // cout << "Decrypting...(private key)" << endl;
        ret = RSA_private_decrypt(
            strData.length(),
            (const unsigned char*)strData.c_str(),
            (unsigned char*)pDecode,
            pRsaKey,
            RSA_PKCS1_PADDING
//            RSA_NO_PADDING
        );
    }

    if(ret >= 0){
        strRet = std::string((char*)pDecode, ret);
    }

    delete [] pDecode;
    RSA_free(pRsaKey);
    fclose(hKeyFile);
    CRYPTO_cleanup_all_ex_data();
    return strRet;
}

void p_help(string self){
    cout << "RSA encypt | decrypt - v2.0" << endl;
    cout << "    " + self + " <KEY_TYPE> <KEY_FILE> <METHOD> <TEXT | -f> [FILE]" << endl;
    cout << "\t<KEY_TYPE> :" << endl;
    cout << "\t    -pub\tUse RSA public key to encrypt or decrypt" << endl;
    cout << "\t    -pri\tUse RSA private key to encrypt or decrypt" << endl;
    cout << "\t<METHOD> :" << endl;
    cout << "\t    -e  \tencrypt text" << endl;
    cout << "\t    -d  \tdecrypt text" << endl;
    cout << "\t<TEXT> :" << endl;
    cout << "\t    PLAIN if method is encypt" << endl;
    cout << "\t    BASE64_ENCODED_CIPHER if method is decypt" << endl;
    cout << "\t    <-f> if read data to encrypt from [FILE]" << endl;
}

int main(int argc, char* argv[])
{
    const string self = argv[0];
    //原文
    if (argc >= 5){
        const char * tmp;
        long fileLen, result;
        string two;
        string text;
        const string keyType = argv[1];
        const string key = argv[2];
        const string md = argv[3];
        const string one = argv[4];
        string binFile;
        bool usePub = true;
        FILE *fp;
        text = one;

        if (keyType == "-pri"){usePub = false;}

        if (md == "-e"){
            if (one == "-f"){
                binFile = argv[5];
                if(fp = fopen(binFile.c_str(), "rb")){
                    fseek(fp, 0L, SEEK_END);
                    fileLen = ftell(fp);
                    rewind(fp);
                    char * fData = (char*)malloc(fileLen + 1);

                    result = fread(fData, 1, fileLen, fp);

                    if (result != fileLen){
                        fputs ("Reading error", stderr);
                        return 0;
                    }
                    text = string(fData, fileLen);
                    fclose(fp);

                }
                else{
                    cout << "Error file!" << endl;
                    return -1;
                }
            }else{
                text = one;
            }

            two = EncodeRSAKeyFile(key, text, usePub);
            tmp = two.c_str();

            string enbase64 = base64_encode((unsigned const char*)tmp, two.length());
            cout << enbase64 << endl;

        }else if(md == "-d"){
            const string two = DecodeRSAKeyFile(key, base64_decode(text), usePub);
            cout << two << endl;
        }else{
            p_help(self);
        }
    }else{
        p_help(self);
    }
    return 0;
}
