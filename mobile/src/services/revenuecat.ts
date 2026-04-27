import Purchases, { PurchasesOffering } from 'react-native-purchases';
import Constants from 'expo-constants';
import { Platform } from 'react-native';

export const initRevenueCat = async () => {
  const apiKey = Platform.select({
    ios: Constants.expoConfig?.extra?.revenueCatIosKey,
    android: Constants.expoConfig?.extra?.revenueCatAndroidKey,
  });

  if (apiKey) {
    Purchases.configure({ apiKey });
  }
};

export const getOfferings = async (): Promise<PurchasesOffering | null> => {
  try {
    const offerings = await Purchases.getOfferings();
    return offerings.current;
  } catch (error) {
    console.error('Error fetching offerings:', error);
    return null;
  }
};

export const purchasePackage = async (packageToPurchase: any) => {
  try {
    const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);
    return customerInfo;
  } catch (error: any) {
    if (!error.userCancelled) {
      console.error('Purchase error:', error);
    }
    throw error;
  }
};

export const restorePurchases = async () => {
  try {
    const customerInfo = await Purchases.restorePurchases();
    return customerInfo;
  } catch (error) {
    console.error('Restore purchases error:', error);
    throw error;
  }
};

export default Purchases;
