import 'import.dart';


Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  print("-----------FirebaseMessaging-----------onBackgroundMessage");
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);
  await dotenv.load(fileName: 'assets/.env');
  runApp(const MyApp());
}