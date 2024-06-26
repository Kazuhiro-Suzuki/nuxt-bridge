// File generated by FlutterFire CLI.
// ignore_for_file: lines_longer_than_80_chars, avoid_classes_with_only_static_members
import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

/// Default [FirebaseOptions] for use with your Firebase apps.
///
/// Example:
/// ```dart
/// import 'firebase_options.dart';
/// // ...
/// await Firebase.initializeApp(
///   options: DefaultFirebaseOptions.currentPlatform,
/// );
/// ```
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError(
        'DefaultFirebaseOptions have not been configured for web - '
        'you can reconfigure this by running the FlutterFire CLI again.',
      );
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        return ios;
      case TargetPlatform.macOS:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for macos - '
          'you can reconfigure this by running the FlutterFire CLI again.',
        );
      case TargetPlatform.windows:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for windows - '
          'you can reconfigure this by running the FlutterFire CLI again.',
        );
      case TargetPlatform.linux:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for linux - '
          'you can reconfigure this by running the FlutterFire CLI again.',
        );
      default:
        throw UnsupportedError(
          'DefaultFirebaseOptions are not supported for this platform.',
        );
    }
  }

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'AIzaSyC0Lh3MotD6lIaRcd3Xwk4uLh5wx3lY3gM',
    appId: '1:876987853030:android:847951a210ac0ec7cf3327',
    messagingSenderId: '876987853030',
    projectId: 'lg-pwd-app-chigasaki',
    storageBucket: 'lg-pwd-app-chigasaki.appspot.com',
  );

  static const FirebaseOptions ios = FirebaseOptions(
    apiKey: 'AIzaSyDlhM4GFQRmeFTIn_W8R1brG5ES8DHVplU',
    appId: '1:876987853030:ios:410471d3caf60341cf3327',
    messagingSenderId: '876987853030',
    projectId: 'lg-pwd-app-chigasaki',
    storageBucket: 'lg-pwd-app-chigasaki.appspot.com',
    iosClientId: '876987853030-fj5h8qjqata7ikhv1j52r6dpb9d6rkub.apps.googleusercontent.com',
    iosBundleId: 'jp.lg-pwd.chigasaki',
  );
}
