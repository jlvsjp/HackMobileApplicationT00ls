package com.fourdogs.signtest;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.codec.digest.DigestUtils;
import java.util.Base64;
import java.lang.StringBuilder;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Collections;

public class signOut{

    public static void main(String[] args){
        String text = "";
        if(args.length == 1){
            text = args[0];
        }else{
            StringBuilder sb = new StringBuilder("Usage:\n\t");
            sb.append("sign_trans_out <payCmaPassWord>");
            System.out.println(sb.toString());
            System.exit(0);
        }
        Map<String, String> mystr = new HashMap<String, String>();
        String b_sign = "8dG1p+ciDbLLCJSrSlKabz9twjdwX/mO";
        mystr.put((String)"payPamaPassWord", "dgs32");
        mystr.put((String)"payCmaPassWord", text);
        mystr.put((String)"channelCode", "PAB");
        mystr.put((String)"channelName", "平安银行");
        mystr.put((String)"channelCardNumber", "6230580000109041496");
        mystr.put((String)"channelCardOwnerName", "郝晋波");
        mystr.put((String)"tagCardId", "39114644");
        mystr.put((String)"amount", "0.5");
        mystr.put((String)"transType", "01");
        try{
            sign(mystr, b_sign);
        } catch (Exception a){;}
    }

    public static void sign(Map<String, String> object, String bf) throws Exception{
        StringBuilder sb = new StringBuilder();
        String data = "";
        if (object == null) System.out.println("Error object : null");
        if (object.size() == 0) System.out.println("Error object - size 0");
        if (!StringUtils.isEmpty((String)bf))
            data = b(object, bf);
            System.out.println("Encoed : \n\t" + data);
            sb.append(Base64.getEncoder().encodeToString((byte[])DigestUtils.sha256((byte[])data.getBytes("UTF-8"))));
            System.out.println("Signature : \n\t" + sb.toString());
    }


    public static String b(Map<String, String> map, String string2) {
        ArrayList<String> arrayList = new ArrayList<String>(map.keySet());
        Collections.sort(arrayList);
        StringBuilder stringBuilder = new StringBuilder("");
        int n2 = 0;
        do {
            if (n2 >= arrayList.size()) {
                stringBuilder.append("&key=").append(string2);
                return stringBuilder.toString();
            }
            String string3 = arrayList.get(n2);
            String string4 = map.get(string3);
            if (StringUtils.isNotEmpty((String)string4)) {
                String string5 = n2 == 0 ? "" : "&";
                stringBuilder.append(string5).append(string3).append("=").append(string4);
            }
            ++n2;
        } while (true);
    }
}
