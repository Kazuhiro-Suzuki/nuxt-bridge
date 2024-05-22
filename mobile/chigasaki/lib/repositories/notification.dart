import '../import.dart';


class NotificationApi {
  static final flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();

  static Future _notificationDetails() async {
    return const NotificationDetails(
      android: AndroidNotificationDetails(
          'high_importance_channel', // id
          'High Importance Notifications', // title
          channelDescription: 'This channel is used for important notifications.', // description
          importance: Importance.high,
      ),
      iOS: DarwinNotificationDetails()
    );
  }

  static Future shownNotification({
    int id = 0,
    String? title,
    String? body,
    // String? payload,
  }) async => flutterLocalNotificationsPlugin.show(
    id,
    title, 
    body,
    await _notificationDetails(),
    // payload: payload
  );

  static Future init(FirebaseMessaging messaging) async {
    const android =  AndroidInitializationSettings('logo_chigasaki');
    const ios =  DarwinInitializationSettings();
    await messaging.requestPermission(
      alert: true,
      badge: true,
      announcement: true,
    );
    await messaging.setForegroundNotificationPresentationOptions(
      alert: true,
      badge: true,
      sound: true,
    );
    flutterLocalNotificationsPlugin.resolvePlatformSpecificImplementation<AndroidFlutterLocalNotificationsPlugin>()?.requestPermission();
    const setting = InitializationSettings(android: android, iOS: ios);
    await flutterLocalNotificationsPlugin.initialize(setting);
  }
} 