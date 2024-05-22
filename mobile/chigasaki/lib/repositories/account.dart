import '../import.dart';
import 'package:http/http.dart' as http;

String baseUrl() {
    if (Platform.isIOS) {
      return dotenv.env['API_URL_IOS'].toString();
    } else {
      return dotenv.env['API_URL_ANDROID'].toString();
    }
}


Future<bool> veriyFirebaseToken(String token) async {
  print('-------veriyFirebaseToken--------- ' + token);
  String url = '${baseUrl()}/api/v1/app/firebase_verify_token/';
  Map<String, String> headers = {'content-type': 'application/json'};
  Map<String, String> body = {'token': token};
  final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(body));
  var decodedData = json.decode(utf8.decode(response.bodyBytes));
  if (response.statusCode == 200) {
    return decodedData['result'];
  }
  return false;
}


Future<int> postFirebaseToken(String token) async {
  print('---------postFirebaseToken---------:' + token);
  String url = '${baseUrl()}/api/v1/app/firebase_token/';
  Map<String, String> headers = {'content-type': 'application/json'};
  Map<String, String> body = {
    'token': token,
    'city_code': '142077',
  };
  final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(body));
  return response.statusCode;
}

  Future<String> getToken(FirebaseMessaging messaging) async {
    var token = await messaging.getToken();
    var result = await veriyFirebaseToken(token.toString());
    // print('----$result----------$token--------------------');
    if (!result) {
      await postFirebaseToken(token.toString());
    } else {
      print('-------------firebase token already exist.----------');
    }
    return token.toString();
  }