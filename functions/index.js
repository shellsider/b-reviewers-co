const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

// Run every 2 weeks
exports.cleanupBlacklistedTokens = functions.pubsub.schedule('every 2 weeks').onRun(async (context) => {
    try {
        const twoWeeksAgo = new Date();
        twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 14);

        // Get reference to the blacklist collection
        const blacklistRef = admin.firestore().collection('token_blacklist');

        // Query for documents older than 2 weeks
        const snapshot = await blacklistRef
            .where('revoked_at', '<', twoWeeksAgo)
            .get();

        if (snapshot.empty) {
            console.log('No tokens to clean up');
            return null;
        }

        // Delete in batches (Firestore has a limit of 500 operations per batch)
        const batchSize = 500;
        const batches = [];
        let batch = admin.firestore().batch();
        let operationCount = 0;

        snapshot.docs.forEach((doc) => {
            batch.delete(doc.ref);
            operationCount++;

            if (operationCount === batchSize) {
                batches.push(batch.commit());
                batch = admin.firestore().batch();
                operationCount = 0;
            }
        });

        // Commit any remaining operations
        if (operationCount > 0) {
            batches.push(batch.commit());
        }

        // Wait for all batches to complete
        await Promise.all(batches);

        console.log(`Successfully deleted ${snapshot.size} blacklisted tokens`);
        return null;
    } catch (error) {
        console.error('Error cleaning up blacklisted tokens:', error);
        return null;
    }
});