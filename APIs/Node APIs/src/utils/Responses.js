module.exports = class {
    async sendBadRequestResponse(message) {
        return {
            status: 400,
            jsonBody: {
                error: message
            }
        };
    };

    async sendInternalServerErrorResponse(message) {
        return {
            status: 500,
            jsonBody: {
                error: message
            }
        };
    };

    async sendAuthFailedResponse(message) {
        return {
            status: 403,
            jsonBody: {
                error: message
            }
        };
    };

    async sendSuccessResponse(json) {
        return {
            status: 200,
            jsonBody: json
        };
    };
};