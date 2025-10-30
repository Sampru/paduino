#include "time.h"

// Convert time to HH:MM:ss string
String epochToString(unsigned long epochTime) {
  String timeStr = "";
  unsigned long tzEpoch = epochTime + 3600;
  unsigned long seconds = tzEpoch % 86400;
  unsigned long hours = seconds / 3600;
  seconds = seconds % 3600;
  unsigned long minutes = seconds / 60;
  seconds = seconds % 60;
  
  if (hours < 10) timeStr += "0";
  timeStr += String(hours);
  timeStr += ":";
  if (minutes < 10) timeStr += "0";
  timeStr += String(minutes);
  timeStr += ":";
  if (seconds < 10) timeStr += "0";
  timeStr += String(seconds);
  
  return timeStr;
}