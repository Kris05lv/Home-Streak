import * as Sentry from '@sentry/react-native';
import Constants from 'expo-constants';

export const initSentry = () => {
  Sentry.init({
    dsn: Constants.expoConfig?.extra?.sentryDsn,
    enableInExpoDevelopment: false,
    debug: __DEV__,
    tracesSampleRate: 1.0,
    environment: __DEV__ ? 'development' : 'production',
  });
};

export const captureException = (error: Error, context?: Record<string, any>) => {
  if (context) {
    Sentry.setContext('error_context', context);
  }
  Sentry.captureException(error);
};

export const captureMessage = (message: string, level: Sentry.SeverityLevel = 'info') => {
  Sentry.captureMessage(message, level);
};

export default Sentry;
