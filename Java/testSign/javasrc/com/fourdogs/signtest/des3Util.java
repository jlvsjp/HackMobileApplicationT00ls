package com.fourdogs.signtest;

import java.util.Arrays;
import java.lang.StringBuilder;
import java.lang.String;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.DESedeKeySpec;
import javax.crypto.spec.IvParameterSpec;
import java.security.Key;
import java.security.spec.AlgorithmParameterSpec;
import java.security.spec.KeySpec;
import java.util.Base64;

// import org.apache.commons.codec.binary.Base64;

public class des3Util{
    private static String key = "AQEFAASCAmEwggJdAgEAAoGBAM4OxRuURtYEfZ0uiFsMVjubj0";
    private static String iv = "01234567";

    public static void main(String[] args){
        String text = "";

        if(args.length == 2){
            text = args[1];
        }else{
            StringBuilder sb = new StringBuilder("Usage:\n\t");
            sb.append(" des3Util -e Plain_to_Encrypt\n\t");
            sb.append(" des3Util -d Plain_to_Decrypt\n\t");
            System.out.println(sb.toString());
            System.exit(0);
        }

        if(args[0].equals("-e"))
            des3Encrypt(text);
        else
            des3Decrypt(text);
    }

    public static void des3Encrypt(String text){
        byte[] r = new byte[1024];
        // Base64 base64 = new Base64();
        String ret = "";
        try{
            DESedeKeySpec object1 = new DESedeKeySpec(key.getBytes());
            SecretKey secretKey = SecretKeyFactory.getInstance("desede").generateSecret((KeySpec)object1);
            Cipher object2 = Cipher.getInstance("desede/CBC/PKCS5Padding");
            object2.init(1, (Key)secretKey, new IvParameterSpec(iv.getBytes()));
            r = object2.doFinal(text.getBytes("utf-8"));
            ret = Base64.getEncoder().encodeToString((byte[]) r);
            System.out.println(ret);
        }catch (Exception e){
            System.out.println("Invalid Key or other errors. - Encrypt error!");
            System.out.println(e.toString());
        }finally {
           System.exit(-1);
        }
    }

    public static void des3Decrypt(String text){
        byte[] r = new byte[1024];
        // Base64 base64 = new Base64();
        r = Base64.getDecoder().decode(text.getBytes());
        try{
            DESedeKeySpec object1 = new DESedeKeySpec(key.getBytes());
            SecretKey secretKey = SecretKeyFactory.getInstance("desede").generateSecret((KeySpec)object1);
            Cipher object2 = Cipher.getInstance("desede/CBC/PKCS5Padding");
            object2.init(2, (Key)secretKey, new IvParameterSpec(iv.getBytes()));
            String ret = new String(object2.doFinal(r));
            System.out.println(ret);
        }catch (Exception e){
            System.out.println("Invalid Key or other errors. - Decrypt error!");
            System.out.println(e.toString());
        } finally {
           System.exit(-1);
        }
    }

    public static String bytes2HexString(byte[] b) {
        String ret = "";
        for (int i = 0; i < b.length; i++) {
            String hex = Integer.toHexString(b[ i ] & 0xFF);
            if (hex.length() == 1) {
                hex = '0' + hex;
            }
            ret += hex.toUpperCase();
        }
        return ret;
    }
}
