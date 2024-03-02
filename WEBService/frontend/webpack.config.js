module.exports = {
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    'vue-style-loader',
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            prependData: `@import "@/assets/_styles.sass";`
                        }
                    }
                ]
            }
        ]
    },
}